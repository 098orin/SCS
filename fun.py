# from email.policy import default
import value
# import json
import time
import os
import sys
from datetime import datetime

import crpt

# from cachetools import cached, TTLCache
from rich.console import Console
import scratchattach as scratch3

console = Console()
old_stdout = sys.stdout

# キャッシュ設定
# cache = TTLCache(maxsize=128, ttl=86400)  # 1日間有効

session = scratch3.login(value.username, value.password)

# datadir = os.path.expanduser ("~").replace(os.sep,'/') + "/SCS_data"
datadir = value.datadir

tw_認証 = dict()
watting = list()

"""def set_log(name):
    return
    global console
    global datadir
    path = datadir + "/log_files/" + name + ".log"
    if not file_exists(path):
        write_file(path, "")
    # ファイルにリダイレクトする
    console = Console(file=open(path, "wt"))
    console.rule(f"Report Generated {datetime.now().ctime()}")"""


def cleanup():
    global old_stdout
    global console
    # 元の標準出力とファイルを閉じる
    sys.stdout = old_stdout
    console.file.close()
    console.log("Cleanup complete.")

def to_txt(number):
    try:
        number = str(number)
        if number == "" or len(number)%2 == 1:
            return " "
        Answer = ""
        txt = "/#0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_+.\\$"
        num = ""
        for i in range(len(str(number))):

            if i%2 != 0:
                num = str(num) + str(number[i])
                Answer = Answer + str(txt[int(num)-10])
            else:
                num = int(number[i])
        return Answer
    except Exception as error:
        console.log("In to_txt():" + error)
        return number

def to_num(intxt):
    Answer = ""
    txt = "/#0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_+.\\$"
    for i in range(len(intxt)):
        if intxt[i] in txt:
            num = 0
            while txt[int(num)] != intxt[i]:
                num = num + 1
            Answer = Answer + str(num+10)
    return Answer


def getcloudvalues(id, i):
    if value.project_client[i] == "sc":
        request = scratch3.get_cloud(id) #Returns a dict with all cloud var values
        del request['time']
    elif value.project_client[i] == "tw":
        request = scratch3.get_tw_cloud(id).get_all_vars() #Returns a dict with all cloud var values
        del request['time']
    
    return request

def response_cloudvalues (repuest, gi):
    console.log(repuest)
    if repuest:
        i = 0
        for n in list(repuest):
            i += 1
            set_cloud(i, response(n, gi), gi)
                            
def response(request, gi, nonces, username=None):
    Answer = ""
    request = str(request)
    request, safe, user = purse_request(request)

    if request != "0": #not None
        if safe:
            if user == "":
                console.log("[red]Error: user is empty[/]")
                console.log("|mode: safe")
                console.log(f"|request: {request}")
                return "0"
            path = datadir + "/password/" + user + "_password.txt"
            key = read_file_lines(path, disp_err=False)[0]
            if not file_exists(path):
                console.log("[red]Error: password file not found[/]")
                console.log("|mode: safe")
                console.log(f"|request: {request}")
                return "0"
            # AADはヘッダ
            # nonceはnoncesから取得
            nonces[user]["client_sequence_number"] += 1
            server_nonce = nonces[user]["server_nonce_iv"] + nonces[user]["server_sequence_number"]
            cliant_nonce = nonces[user]["client_nonce_iv"] + nonces[user]["client_sequence_number"]
            """
            AAD  : pad_right(sequesence_number, 4)
            nonce: str(nonces[user]["server_sequence_number"] + pad_right(nonces[user]["server_nonce_iv"]), 12)
            """
            if cliant_nonce == None or aad == None:
                console.log("[red]Error: nonce or aad is None[/]")
                console.log("|mode: safe")
                console.log(f"|request: {request}")
                console.log(f"|user: {user}")
                console.log("||User may not be logged in by password.")
                return "0"
            request = crpt.decrypt_chachapoly(key, request, cliant_nonce, aad)
        
        code = request[0:3]
        req = to_txt(request[3:])

        user = ""
        for i in range(len(req)):
            if req[i] == "/":
                break
            user = user + req[i]
        user = str(user)
        
        temp = i + 1
        var = ""
        for i in range(len(req)-temp):
            i += temp
            if req[i] == "/":
                break
            var = req[i] + var
        
        server_id = ""
        for i in range(len(req)): 
            i = len(req) - i
            i -= 1
            if req[i] == "/":
                break
            server_id = req[i] + server_id
        console.log(req)
        console.log(code)
        console.log(user)
        correct_server_id = value.username + "#"
        if server_id[:len(correct_server_id)] != correct_server_id and server_id != "all":
            console.log("[red]400 Bad request[/]")
            console.log("||サーバー管理者の方は`value.py`に適切なproject id を設定しているか確認してください。")
            console.log("||project id が正しい場合、プロジェクトに不備がある可能性があります。")
            console.log("||プロジェクトの初期化関数を確認してください。")
            Answer = str(user) + to_num("/" + "-1")
            console.log(server_id)
            return ""
        cliant_version = server_id[len(correct_server_id):]
        if safe:
            header = "2"
        else:
            header = "1"
        header = header + "1"
        if code[0] != "1":
            try:
                id = str(user)
                path = datadir + "/about/" + id + "/username.txt"
                if file_exists(path):
                    user = read_file_lines(path, disp_err=False)[0]
            except Exception as error:
                console.log("In response():" + error)

        if code[0] == "1":
            # no id
            header = header[0] + "0"
            console.log('no id')
            if code == "100":
                console.log("get id")

                path = datadir + "/id/" + user + ".txt"
                id = read_file(path)
                if not file_exists(path):
                    Answer = user + "/-1"
                else:
                    path = datadir + "/about/" + id + "/username.txt"
                    if not file_exists(path):
                        write_file(path, user)
                    Answer = user + "/" + str(id)

            elif code == "101":
                # make id
                console.log ("make id") 
                if value.project_privilege[gi] != "high":
                    console.log("Error: projectに十分な権限がありません")
                    Answer = user + "/-1"
                    console.log(Answer)
                    return Answer
                path = datadir + "/id/" + user + ".txt"
                console.log(path)
                if os.path.isfile(path):
                    Answer = user + "/-0"
                else:
                    id = count_files(datadir + "/id/") + 1
                    write_file(path, id)
                    path = datadir + "/about/" + str(id) + "/about.txt"
                    console.log(path)
                    content = "1\n100"
                    write_file(path, content)
                    Answer = user + "/" + str(id)

            elif code == "110":
                path = datadir + "/password/" + user + "_password.txt"
                password = read_file(path)
                aad = pad_right(len(user), 4)
                nonce = pad_right(days_since_2000(), 24)
                if not file_exists(path):
                    Answer = user + "/$$-0"
                    return Answer
                passvar = crpt.decrypt_chachapoly(password, req, nonce, aad)
                if password == passvar:
                    console.log("パスワードが一致しました。セッションを作成します。")
                    sessionid = os.urandom(24).hex() #sessionid は nonce_iv
                    all_sessionid = read_file_lines(datadir + "/session/all_ids.txt")
                    all_sessionuser = read_file_lines(datadir + "/session/all_users.txt")
                    all_sessiontimestamp = read_file_lines(datadir + "/session/all_timestamps.txt")
                    if user in all_sessionuser:
                        console.log("すでにセッションが存在しています。")
                        sessionid = all_sessionid[all_sessionuser.index(user)]
                    else:
                        while sessionid in all_sessionid:
                            sessionid = os.urandom(24).hex()
                        all_sessionid.append(str(sessionid))
                        all_sessionuser.append(user)
                        all_sessiontimestamp.append(str(days_since_2000()))
                        write_file(datadir + "/session/all_ids.txt", all_sessionid)
                        write_file(datadir + "/session/all_users.txt", all_sessionuser)
                        write_file(datadir + "/session/all_timestamps.txt", all_sessiontimestamp)
                        nonces[user] = {
                            "server_nonce_iv": int(str(sessionid)[0:12]),
                            "server_sequence_number": 0,
                            "client_nonce_iv": int(str(sessionid)[12:24]),
                            "client_sequence_number": 0,
                        }
                    Answer = user + "/1/" + str(sessionid)
                    header = "2" # 暗号化用にヘッダーを更新
                    safe = True
                else:
                    console.log("パスワードが間違っています")
                    Answer = user + "/$$-1"
            elif code == "111":
                console.log("TODO")
                pass
            else:
                console.log("未定義")
                         
        elif code[0] == "2":
            # have id
            console.log("have id")
            # 未実装
            if code[2] == "0":
                console.log("get status")
                path = datadir + "/about/" + id + "/about.txt"
                if file_exists(path):
                    file = str(read_file_lines(path)[0])
                else:
                    file = None
                if file == None:
                    Answer = id + "/-0"
                else:
                    Answer = id + "/" + file
                        
            elif code[2] == "1":
                console.log("get point")
                path = datadir + "/about/" + id + "/about.txt"
                if file_exists(path):
                    file = str(read_file_lines(path)[1])
                else:
                    file = None
                if file == None:
                    Answer = id + "/-0"
                else:
                    Answer = id + "/" + file
            elif code[2] == "2":
                # TO DO
                console.log("TO DO")


        elif code[0] == "3":
            console.log ("global file")
            if code[2] == "0":
                console.log("look file")

                # 未実装

            elif code[2] == "1":
                console.log("== file ? (bool)")

                # 未実装
            elif code == "302":
                console.log("count files")
                path = datadir + "/global/" + var
                Answer = id + "/" + str(count_files(path))

            elif code[2] == "3":
                console.log("list files")

                # 未実装


                
        elif code[0] == "4":
            console.log("projects file")
            if code[2] == "0":
                console.log("look file")

                # 未実装

            elif code[2] == "1":
                console.log("== file ? (bool)")

                # 未実装
            elif code == "402":
                console.log("count files")
                path = datadir + "/projects/" + var
                Answer = id + "/" + str(count_files(path))
                
        elif code[0] == "5":
            if code[2] == "0":
                console.log ("mkdir")

                # 未実装
                    
            elif code[2] == "1":
                console.log("to do")

        elif code[0] == "6":
            console.log("point")
            if code[2] == "0":
                console.log("get log-in point")
                if value.project_privilege[gi] != "high":
                    console.log("Error: projectに十分な権限がありません")
                    Answer = id + "/-1"
                    console.log(Answer)
                    return Answer
                path = datadir + "/about/" + id + "/login.txt"
                if file_exists(path):
                    logintime = float(read_file_lines(path)[0])
                else:
                    logintime = 0.0
                    write_file(path, "0")
                if time.time()/86400 - logintime >= 1.0:
                    console.log("ログインポイントを更新")
                    path = datadir + "/about/" + id + "/about.txt"
                    file = read_file_lines(path)[1]
                    Answer = id + "/" + str(float(file) + 3.0)

                    f = open(path, "w")
                    f.write(str(file[0].rstrip()) + "\n" + str(float(file) + 3.0) )
                    f.close

                    console.log("上書き")
                    file = open(datadir + "/about/" + id + "/login.txt", "w")
                    file.write(str(time.time()/86400))
                    file.close()
                else:
                    Answer = id + "/" + "-1"
        if safe:
            nonces[user]["server_sequence_number"] += 1
            # responseを暗号化
            key = read_file_lines(datadir + "/password/" + user + "_password.txt", disp_err=False)[0]
            nonce = str(nonces[user]["server_sequence_number"] + pad_right(nonces[user]["server_nonce_iv"]), 12)
            aad = pad_right(nonces[user]["server_sequence_number"], 4)
            Answer = crpt.encrypt_chachapoly(
                key,
                to_num(Answer),
                nonce,
                aad,
            )

        console.log(header + ", " + Answer)
        return header + to_num(Answer), nonces


def purse_request(request):
    if request == "0":
        return "0", False, ""
    if request[0:2] == "11":
        return str(request[2:]), False, ""
    elif request[0:2] == "10":
        serverid = ""
        user = ""
        request = str(request[2:])
        i = len(request)
        while request[i-2:i] != "10":
            serverid = request[i-2:i] + serverid
            i -= 2
        while request[i-2:i] != "10":
            user = request[i-2:] + user
            i -= 2
        serverid = to_txt(serverid)
        user = to_txt(user)
        correct_id = value.username + "#"
        if serverid[:len(correct_id)] != correct_id:
            return "0", False, ""
        return str(request[0:i]), True, user
    else:
        return "0", False, ""

def set_cloud (n,num:int, gi):
    if num == None:
        return "None"
    try:
        conn = session.connect_cloud(value.project_id[gi])
        if value.project_client[gi] == "sc":
            conn = session.connect_cloud(value.project_id[gi])
        elif value.project_client[gi] == "tw":
            msg ="SCS project server by" + value.username + " on Scratch"
            conn = scratch3.get_tw_cloud(value.project_id[gi], contact=msg)
        conn.set_var(n,num)
    except Exception as error:
        console.log("Error: " + str(error))

def count_files(path) -> int:
    # ディレクトリ内のファイルをカウントする
    try:
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return len(files)
    except FileNotFoundError:
        console.log("指定したパスが見つかりません。")
        return 0

def write_file(path, txt):
    # 指定したパスにテキストファイルを作成して内容を書き込む
    txt = str(txt)
    # ディレクトリが存在しない場合は作成する
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, 'w') as file:
            file.write(txt)
        console.log(f"{path} にファイルを作成")
    except Exception as e:
        console.log(f"Error: {e}")

def read_file(path):
    """
    指定したパスのファイルを読み込む

    Args:
        path: ファイルパス

    Returns:
        ファイルの内容。なかったら何も返さず、エラーメッセージを表示する。
    """
    try:
        with open(path, 'r') as file:  # 'r'モードで読み込み
            content = file.read()  # ファイルの全内容を読む
        return content
    except FileNotFoundError:
        console.log(f"{path} は見つかりませんでした。")
    except Exception as e:
        console.log(f"エラーが発生しました: {e}")

def read_file_lines(file_path, disp_err=True):
    try:
        with open(file_path, 'r') as file:  # 'r'モードで読み込み
            lines = file.readlines()  # 各行をリストとして読む
        return lines
    except FileNotFoundError:
        if disp_err:
            console.log(f"{file_path} は見つかりませんでした。")
    except Exception as e:
        if disp_err:
            console.log(f"エラーが発生しました: {e}")

def file_exists(path):
  return os.path.exists(path)

def days_since_2000(tofloat=False):
    # 2000年1月1日午前0時0分0秒をUTCで定義
    start_date = datetime(2000, 1, 1, 0, 0, 0)
    
    # 現在のUTC時間を取得
    current_date = datetime.utcnow()
    
    # 経過日数を計算
    delta = current_date - start_date
    if tofloat:
        return delta.days
    else:
        return int(delta.days)

def pad_right(text: str, total_length: int, pad_char: str = 'f') -> str:
    """
    文字列の右側を指定した文字で埋めて指定した長さにする

    Args:
        text: 埋めたい文字列
        total_length: 埋めた後の文字列の目標の長さ
        pad_char: 埋める文字 (デフォルトは"f")

    Returns:
        右側を指定した文字で埋めた文字列
    """
    if len(text) > total_length:
        return text[:total_length]
    else:
        return text.ljust(total_length, pad_char)