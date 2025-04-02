import tools

tools.install_if_not_exists("cryptography")
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
"""
# 秘密鍵、nonce、追加認証データ（AAD）を用意
key = b'secret_key_must_be_32_bytes' # 32バイトの秘密鍵だよ
nonce = b'nonce_must_be_12_bytes'  # 12バイトのnonce
associated_data = b'authenticated_data'  # AAD
"""

# 暗号化！
def encrypt(data, key, nonce, associated_data):
    cipher = Cipher(algorithms.ChaCha20Poly1305(key, nonce), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    encryptor.authenticate_additional_data(associated_data)  # AAD認証
    ciphertext = encryptor.update(data) + encryptor.finalize()
    tag = encryptor.tag  # タグ
    return ciphertext, tag

# 復号！
def decrypt(ciphertext, tag, key, nonce, associated_data):
    cipher = Cipher(algorithms.ChaCha20Poly1305(key, nonce, tag), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    decryptor.authenticate_additional_data(associated_data)  # AAD認証
    try:
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext
    except:
        return None  # 認証に失敗したらNoneを返す

# 実行！
"""
data = b'Hello, cute world!'
ciphertext, tag = encrypt(data, b'secret_key_must_be_32_bytes', b'nonce_must_be_12_bytes', b'authenticated_data')
decrypted_data = decrypt(ciphertext, tag, b'secret_key_must_be_32_bytes', b'nonce_must_be_12_bytes', b'authenticated_data')

if decrypted_data:
    print("元データ:", data)
    print("復号データ:", decrypted_data)
else:
    print("復号失敗...")"
"""