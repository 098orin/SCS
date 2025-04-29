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
