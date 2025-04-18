import os
import requests

version = "2.0 - β.2.1"
print("Server version: v." + version)

try:
    if os.geteuid() == 0:
        print("管理者権限で実行中です")
    else:
        print("非管理者権限で実行中です")
except Exception as error:
        print(error)

print("更新を確認...")
url = "https://raw.githubusercontent.com/098orin/SCS/main/README.md"
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

print("サーバーを起動中...")

# import main
import value
# import concurrent.futures
# import time
import tools

tools.install_if_not_exists("cryptography")
tools.install_if_not_exists("scratchattach")

path = value.path

file = open(path + "/fun.py", "br")
fun_hash_old = hash(file.read())
file.close()

file = open(path + "/value.py", "br")
val_hash_old = hash(file.read())
file.close()

i = 1
print("Done!")

import threading
import subprocess
import sys
import signal
import time

coms = []
threads = []
processes = []

def signal_handler(sig, frame):
    print("\nサーバーを終了します...")

    for process in processes:
        process.terminate() # プロセスを終了する

    print("サーバーを正常に終了しました。")
    sys.exit(0)

# シグナルハンドラの設定
signal.signal(signal.SIGINT, signal_handler)

for i in range(len(value.project_id)):
    com = f"python {value.path}/event.py {i}"
    coms.append(com)
print(coms)

# スレッドを作成してプロセスを実行
while True:
    for cmd in coms:
        process = subprocess.Popen(cmd, shell=True, text=True)
        processes.append(process)  # プロセスをリストに追加

        thread = threading.Thread(target=process.wait)  # プロセスが終了するのを待つスレッド
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    time.sleep(10)

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