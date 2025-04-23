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

file = open(path + "/fun.py", "br")
fun_hash_old = hash(file.read())
file.close()

file = open(path + "/value.py", "br")
val_hash_old = hash(file.read())
file.close()

i = 1

from rich.progress import Progress

import threading
import subprocess
import sys
import signal
import time

coms = []
threads = []
processes = []

def cleanup():
    print("\nCtrl+C を検知。サーバーを終了します...")
    for process in processes:
        if process.poll() is None:  # プロセスがまだ実行中なら
            process.terminate()
            process.kill()  # 強制終了
    print("Waiting for threads to finish...")
    for thread in threads:
        thread.join(timeout=5) # スレッドの終了を待つ
    print("サーバーを正常に終了しました。")

# Ctrl+C を検知するためのシグナルハンドラ
def signal_handler(signum, frame):
    cleanup()
    sys.exit(0)

# シグナルハンドラの設定
signal.signal(signal.SIGINT, signal_handler)

for i in range(len(value.project_id)):
    com = f"python {value.path}/event.py {i}"
    coms.append(com)
print(coms)
# スレッドを作成してプロセスを実行
try:
    while True:
        for cmd in coms:
            process = subprocess.Popen(cmd, shell=True, text=True)
            processes.append(process)  # プロセスをリストに追加

            thread = threading.Thread(target=process.wait)  # プロセスが終了するのを待つスレッド
            threads.append(thread)
            thread.start()
        print("Done!")

        for thread in threads:
            thread.join()

        time.sleep(5)
except KeyboardInterrupt:
    cleanup()
    sys.exit(0)
# print("サーバーを終了しました。")


"""
def run_task(i):
        try:
            main.main(value.project_id[i],i)
        except Exception as error:
            print(error)

while True:
    i += 1
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(value.project_id)) as executor:
        futures = [executor.submit(run_task, i) for i in range(len(value.project_id))]  # スレッドを立ち上げ

        # 全ての結果を取得するまで待機
        results = [f.result() for f in concurrent.futures.as_completed(futures)]



    if i == 50:
        i = 0
        try:

            with open(path + "/fun.py", "br") as file:
                fun_hash_new = hash(file.read())
                if fun_hash_old!= fun_hash_new:
                    import main
                    fun_hash_old = fun_hash_new
        
            with open(path + "/value.py", "br") as file:
                val_hash_new = hash(file.read())
                if val_hash_old!= val_hash_new:
                    import main
                    import value
                    val_hash_old = val_hash_new

        except Exception as error:
            print(error)
"""