import os

'''
import subprocess
import time

# リポジトリのURLとディレクトリを指定
repo_url = "https://github.com/your_username/your_repository.git"
local_dir = "/path/to/your/repository"

# 定期的にリポジトリを監視し、更新があればpullして再実行する
while True:
    # 最新の情報を取得
    subprocess.run(["git", "fetch"], cwd=local_dir)

    # ローカルの最新コミットを取得
    local_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=local_dir).strip()

    # リモートの最新情報を取得
    subprocess.run(["git", "remote", "update"], cwd=local_dir)

    # リモートの最新コミットを取得
    remote_commit = subprocess.check_output(["git", "rev-parse", "origin/master"], cwd=local_dir).strip()

    # ローカルとリモートのコミットを比較
    if local_commit != remote_commit:
        print("Updating repository...")
        subprocess.run(["git", "pull"], cwd=local_dir)
        print("Repository is up to date. Restarting the program...")
        
        # ここで再実行するコマンドを指定
        subprocess.run(["python", "your_program.py"], cwd=local_dir)  # 例: 再実行するPythonプログラムを指定

    # 30秒ごとに監視
    time.sleep(30)
'''

"""
repuest = {'2': '101312121018121620181717181814191613141413141210', }

n = str(2)

print(repuest[n])
"""


user = 34223942324235351416
datadir = os.path.expanduser ("~") + "/SCStest"

print ("make id") 
path = datadir + "/id/" + str(user) + ".txt"
print(path)
if not os.path.isfile(path):
    path = datadir + "/id/"
    id = sum(os.path.isfile(os.path.join(path, name)) for name in os.listdir(path))
    id = id + 1
    print(sum(os.path.isfile(os.path.join(path, name)) for name in os.listdir(path)))
    path = path + str(user) + ".txt"
    with open(path, mode='w') as file:
        file.write(str(id))
    path = datadir + "/about/" + str(id) + "/about.txt"
    print(path)
if not os.path.exists(os.path.dirname(path)):
    os.makedirs(os.path.dirname(path))
if not os.path.isfile(path):
        with open(path, mode='w', newline="\n") as file:
            file.writelines( "1\n" + "100" )
