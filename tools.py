import importlib.util
import subprocess
import sys

def install_if_not_exists(package_name: str):
    spec = importlib.util.find_spec(package_name)
    if spec is not None:
        pass
    else:
        print(f"パッケージ '{package_name}' が見つかりません。インストールを開始します...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"パッケージ '{package_name}' のインストールが完了しました。")
        except subprocess.CalledProcessError:
            print(f"パッケージ '{package_name}' のインストールに失敗しました。")
        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")

def hex_to_bytes(hex_str: str) -> bytes:
    return bytes.fromhex(hex_str)
