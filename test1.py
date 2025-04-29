import hashlib
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import (
    Encoding, PublicFormat,
)

# secp256k1 parameters (we need p and n by hand)
_P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def _mod_sqrt(a: int, p: int = _P) -> int:
    """
    Tonelli‐Shanks simplified for p ≡ 3 mod 4:
      sqrt(a) ≡ a^((p+1)//4) mod p
    """
    x = pow(a, (p + 1) // 4, p)
    if (x * x) % p != a % p:
        raise ValueError("no sqrt")
    return x

def derive_privkey_from_password(password: str) -> ec.EllipticCurvePrivateKey:
    """
    SHA256(password) mod n → use that as the private scalar
    """
    h = hashlib.sha256(password.encode("utf-8")).digest()
    sk = int.from_bytes(h, "big") % _N
    if sk == 0:
        sk = 1
    return ec.derive_private_key(sk, ec.SECP256K1())

def pubkey_x_bytes_from_password(password: str) -> bytes:
    """
    Return 32-byte big‐endian X coordinate of the public key
    """
    priv = derive_privkey_from_password(password)
    x = priv.public_key().public_numbers().x
    return x.to_bytes(32, "big")

def _pubkey_from_x_bytes(xb: bytes) -> ec.EllipticCurvePublicKey:
    """
    Reconstruct an EC public key from its X coordinate by solving y^2 = x^3 + 7 mod p.
    We pick the even‐parity root.
    """
    x = int.from_bytes(xb, "big")
    y2 = (pow(x, 3, _P) + 7) % _P
    y = _mod_sqrt(y2, _P)
    # pick even‐parity
    if y & 1:
        y = _P - y
    nums = ec.EllipticCurvePublicNumbers(x, y, ec.SECP256K1())
    return nums.public_key()

def _derive_keystream_blocks(shared: bytes, n_chars: int) -> list:
    """
    Turn a 32-byte shared secret into n_chars of 16-bit words by
    SHA256 chaining:
       K0 = SHA256(shared)
       K1 = SHA256(K0)
       … until you have 2*n_chars bytes
    then split into n_chars of 2‐byte big‐endian ints.
    """
    buf = b""
    last = shared
    while len(buf) < 2 * n_chars:
        last = hashlib.sha256(last).digest()
        buf += last
    return [int.from_bytes(buf[2*i:2*i+2], "big") for i in range(n_chars)]

def encrypt(recipient_pub_x: bytes, plaintext: str) -> bytes:
    """
    recipient_pub_x: 32 bytes, big-endian X coordinate
    plaintext: a Python str (will be UTF-8‐encoded per‐character as ord(c) 0–0x10FFFF)
    
    returns: eph_pub(65) ∥ ciphertext(2*len(plaintext))
    """
    # 1) rebuild recipient pubkey
    rec_pub = _pubkey_from_x_bytes(recipient_pub_x)

    # 2) ephemeral keypair
    eph_priv = ec.generate_private_key(ec.SECP256K1())
    eph_pub = eph_priv.public_key().public_bytes(
        Encoding.X962, PublicFormat.UncompressedPoint
    )  # 65 bytes: 0x04||X(32)||Y(32)

    # 3) ECDH raw secret
    shared = eph_priv.exchange(ec.ECDH(), rec_pub)

    # 4) keystream of 16-bit words
    blocks = _derive_keystream_blocks(shared, len(plaintext))

    # 5) encrypt each character
    ct = bytearray()
    for c, k in zip(plaintext, blocks):
        v = (ord(c) + k) & 0xFFFF
        ct += v.to_bytes(2, "big")

    # 6) return ephemeral pub||ct
    return eph_pub + bytes(ct)

def decrypt(recipient_priv: ec.EllipticCurvePrivateKey, data: bytes) -> str:
    """
    data = eph_pub(65) ∥ ci
phertext(2*N)
    returns the recovered plaintext str
    """
    eph_pub = ec.EllipticCurvePublicKey.from_encoded_point(
        ec.SECP256K1(), data[:65]
    )
    ct = data[65:]
    n = len(ct) // 2

    # ECDH
    shared = recipient_priv.exchange(ec.ECDH(), eph_pub)

    # keystream
    blocks = _derive_keystream_blocks(shared, n)

    # decrypt
    chars = []
    for i in range(n):
        v = int.from_bytes(ct[2*i:2*i+2], "big")
        p = (v - blocks[i]) & 0xFFFF
        chars.append(chr(p))
    return "".join(chars)

# — example of use —
if __name__ == "__main__":
    # password→keypair
    pw = "correct horse battery staple"
    priv = derive_privkey_from_password(pw)
    pub_x = pubkey_x_bytes_from_password(pw)

    msg = "Hello, world!"
    blob = encrypt(pub_x, msg)

    got = decrypt(priv, blob)
    assert got == msg
    print("OK:", got)