import os
import requests
import ctypes

version = "2.0β"
print("Server version: v." + version)

def is_admin():
    if os.name == "nt":
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    else:
        return os.geteuid() == 0

try:
    if is_admin():
        print("管理者権限で実行中です")
    else:
        print("非管理者権限で実行中です")
        print("管理者権限で実行することが推奨されています")
except Exception as e:
    print("実行権限の確認中にエラーが発生しました")
    print(f"Error: {e}")

print("更新を確認...")
url = "https://raw.githubusercontent.com/098orin/SCS/main/README.md"
try:
    response = requests.get(url)
    if response.status_code == 200: # ステータスコードを確認
        f_line = response.text.splitlines()[0]
        now_version = f_line[10:len(f_line)]
        if now_version != version:

            print("新しいバージョンがあります: v." + now_version)
            print("新しいバージョンをインストールしますか?(y/n)")
            an = input()
            if an.lower() == "y":
                try:
                    os.system("sudo git pull")
                    print("プログラムを更新しました。")
                except:
                    try:
                        os.system("git pull")
                        print("プログラムを更新しました。")
                    except Exception as error:
                        print(f"Error: error")
        else:
            print("更新はありません。")
    else:
        print(f"Error: {response.status_code}")
except Exception as e:
    print("更新の確認中にエラーが発生しました")
    print(f"Error: {e}")

print("Don't shutdown the program before the listener is set up.")
print("イベントリスナーのセッティングが完了するまで絶対にサーバーを終了させないでください。")

print("\nサーバーを起動中...")

import value
import tools

tools.install_if_not_exists("cryptography")
tools.install_if_not_exists("scratchattach")
tools.install_if_not_exists("rich")

path = value.path

"""file = open(path + "/fun.py", "br")
fun_hash_old = hash(file.read())
file.close()

file = open(path + "/value.py", "br")
val_hash_old = hash(file.read())
file.close()"""

i = 1

import subprocess
import time
import sys
import threading
from rich.console import Console
from rich.logging import RichHandler
import logging
import value

# Richのコンソール設定
console = Console()
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console, show_path=False)],
)
log = logging.getLogger("rich")

def run_process(commands, process_name):
    """
    単一のコマンドを実行し、その状態を監視する。

    Args:
        command (list): 実行するコマンド
        process_name (str): プロセスの名前（ログ出力用）
    """
    log_file = f"{value.datadir}/log_files/{process_name}.log"
    command_ver = 0 
    while True:
        command = commands[command_ver]
        log.info(f"[bold green]{process_name}[/]: プロセスを開始: {command}", extra={"markup": True})
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            while True:
                output = process.stdout.readline()
                if output:
                    # コンソールに直接出力
                    console.log(f"[bold green]{process_name}[/] [stdout] {output.strip()}", extra={"markup": True})
                    with open(log_file, "a") as f:
                        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [{process_name}] [stdout] {output.strip()}\n")

                error = process.stderr.readline()
                if error:
                    # コンソールに直接出力
                    console.log(f"[bold red]{process_name}[/] [stderr] {error.strip()}", extra={"markup": True})
                    with open(log_file, "a") as f:
                        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [{process_name}] [stderr] {error.strip()}\n")


                if process.poll() is not None:
                    break

            return_code = process.returncode
            if return_code == 0:
                log.info(f"[bold green]{process_name}[/] プロセスが正常終了しました。再起動します...")
            else:
                log.error(f"[bold red]{process_name}[/] プロセスが異常終了しました（コード: {return_code}）。再起動します...")
            with open(log_file, "a") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [{process_name}] プロセス終了、コード: {return_code}\n")
        except FileNotFoundError as e:
            command_ver = 1
            log.error(f"[bold red]{process_name}[/] エラー発生: {e}", extra={"markup": True})
        except Exception as e:
            log.error(f"[bold red]{process_name}[/] エラー発生: {e}", extra={"markup": True})
            with open(log_file, "a") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [{process_name}] エラー発生: {e}\n")

        time.sleep(5)


def main():
    coms = []
    names = []
    for i in range(len(value.project_id)):
        com = [f"python {value.path}/event.py {i}", f"python event.py {i}"]
        coms.append(com)
        names.append(f"{value.project_client[i]}_{value.project_id[i]}_eventpy")
    print(coms)

    threads = []
    for i in range(len(coms)):
        thread = threading.Thread(
            target=run_process,
            args=(coms[i], names[i]),
            daemon=True
        )
        threads.append(thread)
        thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log.info("終了シグナルを受け取りました。")
        sys.exit(0)


if __name__ == "__main__":
    main()