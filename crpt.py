from unittest.util import strclass
import tools

tools.install_if_not_exists("cryptography")
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.exceptions import InvalidTag

# --- 暗号化関数 ---
def encrypt_data(key: bytes, plaintext: bytes, nonce: bytes, aad: bytes = None) -> str:
    """
    ChaCha20-Poly1305 を使ってデータを暗号化するよ！

    Args:
        key: 暗号化に使うキー (32バイト)
        plaintext: 暗号化したいデータ (バイト列)
        nonce: nonce (12バイト)
        aad: 付加認証データ (オプション、バイト列)

    Returns:
        ciphertext: 暗号化されたデータと認証タグ (バイト列)
    """

    # ChaCha20Poly1305 オブジェクトを作成するよ キーを渡す
    aead = ChaCha20Poly1305(key)

    # encrypt() メソッドで暗号化 nonce, plaintext, aad を渡す
    ciphertext = aead.encrypt(nonce, plaintext, aad)

    # 暗号化されたデータを返す
    return ciphertext.hex()

# --- 復号化関数 ---
def decrypt_data(key: bytes, nonce: bytes, ciphertext: bytes, aad: bytes = None) -> str | None:
    """
    ChaCha20-Poly1305 を使ってデータを復号化するよ！

    Args:
        key: 復号化に使うキー (32バイト)
        nonce: 暗号化時に使われた nonce (12バイト)
        ciphertext: 暗号化されたデータと認証タグ (バイト列)
        aad: 付加認証データ (オプション、バイト列)

    Returns:
        復号化されたデータ (HEX列)。認証に失敗した場合は None を返すよ。
    """
    # ChaCha20Poly1305 オブジェクトを作成するよ！ キーを渡すんだ。
    aead = ChaCha20Poly1305(key)

    try:
        # decrypt() メソッドで復号化！ nonce, ciphertext, aad を渡すよ。
        # 認証に失敗すると InvalidTag が発生するんだ。
        decrypted_plaintext = aead.decrypt(nonce, ciphertext, aad)

        # 復号化に成功したらデータを返すよ！
        return decrypted_plaintext.hex()

    except InvalidTag:
        # 認証に失敗した場合は None を返すか、例外を再 raise するか選び方があるけど
        # 今回は None を返すようにしてみたよ。
        print("⚠ 認証に失敗しました！ データが改ざんされた可能性があります。")
        return None