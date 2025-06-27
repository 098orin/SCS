from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.exceptions import InvalidTag

# from fun import pad_right

# --- 暗号化関数 ---
def encrypt_chachapoly(key: bytes, plaintext: bytes, nonce: bytes, aad: bytes = None) -> str:
    """
    ChaCha20-Poly1305 を使ってデータを暗号化する

    Args:
        key: 暗号化に使うキー (32バイト)
        plaintext: 暗号化したいデータ (バイト列)
        nonce: nonce (12バイト)
        aad: 付加認証データ (オプション、バイト列)

    Returns:
        ciphertext: 暗号化されたデータと認証タグ (バイト列)
    """
        # Byteでなかったら変換
    if isinstance(key, bytes):
        key = bytes.fromhex(key)
    if isinstance(plaintext, bytes):
        plaintext = bytes.fromhex(plaintext)
    if isinstance(nonce, bytes):
        nonce = bytes.fromhex(nonce)
    if isinstance(aad, bytes):
        aad = bytes.fromhex(aad)

    # ChaCha20Poly1305 オブジェクトを作成し、キーを渡す
    aead = ChaCha20Poly1305(key)

    # encrypt() メソッドで暗号化 nonce, plaintext, aad を渡す
    ciphertext = aead.encrypt(nonce, plaintext, aad)

    # 暗号化されたデータを返す
    return ciphertext.hex()

# --- 復号化関数 ---
def decrypt_chachapoly(key, ciphertext, nonce, aad = None) -> str | None:
    """
    ChaCha20-Poly1305 を使ってデータを復号化する

    Args:
        key: 復号化に使うキー (32バイト)
        ciphertext: 暗号化されたデータと認証タグ (バイト列)
        nonce: 暗号化時に使われた nonce (12バイト)
        aad: 付加認証データ (オプション、バイト列)

    Returns:
        復号化されたデータ (HEX列)。認証に失敗した場合は None を返す
    """
    # Byteでなかったら変換
    if isinstance(key, str):
        key = bytes.fromhex(key)
    if isinstance(ciphertext, str):
        ciphertext = bytes.fromhex(ciphertext)
    if isinstance(nonce, str):
        nonce = bytes.fromhex(nonce)
    if isinstance(aad, str):
        aad = bytes.fromhex(aad)
    # ChaCha20Poly1305 オブジェクトを作成 キーを渡す
    aead = ChaCha20Poly1305(key)

    try:
        # decrypt() メソッドで復号化 nonce, ciphertext, aad を渡す
        # 認証に失敗すると InvalidTag が発生する
        decrypted_plaintext = aead.decrypt(nonce, ciphertext, aad)

        # 復号化に成功したらデータを返す
        return decrypted_plaintext.hex()

    except InvalidTag:
        # 認証に失敗した場合 None を返す
        print("⚠ 認証に失敗しました！ データが改ざんされた可能性があります。")
        return None