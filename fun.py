# from email.policy import default
import value
# import global_value as g
import json
import time
import os
from datetime import datetime

import crpt

import scratchattach as scratch3

# global i2

pdata = {}

session = scratch3.login(value.username, value.password)

# datadir = os.path.expanduser ("~").replace(os.sep,'/') + "/SCS_data"
datadir = value.datadir

tw_認証 = dict()
watting = list()

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
        print("In to_txt():" + error)
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
    print(repuest)
    if repuest:
        i = 0
        for n in list(repuest):
            i += 1
            set_cloud(i, response(n, gi), gi)
                            
def response(request, gi):
    Answer = ""
    request = str(request)
    request, safe = purse_request(request)

    if request != "0": #not None
        code = request[0:3]
        req = to_txt(request[3:len(request)])
        print(req)

        user = ""
        for i in range(len(req)):
            if req[i] == "/":
                break
            user = user + req[i]
        user = str(user)
        
        temp = i + 1
        var = ""
        for i in range(len(req)):
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

        if server_id != value.username and server_id != "all":
            print("400 Bad request")
            print("サーバー管理者の方は`value.py`に適切なproject id を設定しているか確認してください。")
            print("project id が正しい場合、プロジェクトに不備がある可能性があります。")
            print("プロジェクト側の@server_idが正しく自分の`value.py`のusernameと一致していることを確認してください。")
            print("===")
            Answer = str(user) + to_num("/" + "-1")
            print(req)
            print(code)
            print(user)
                
        if code[0] == "1":
            # no id
            print('no id')
            if code[1] == "0":
                if code[2] == "0":
                    path = datadir + "/id/" + user + ".txt"
                    id = read_file(path)
                    if id == None:
                        pass

                elif code == "101":
                    # make id
                    print ("make id") 
                    if value.project_privilege[gi] != "high":
                        print("Error: projectに十分な権限がありません")
                        Answer = to_num(user + "/-1")
                        print(Answer)
                        return Answer
                    path = datadir + "/id/" + user + ".txt"
                    print(path)
                    if os.path.isfile(path):
                        Answer = to_num(user + "/-1")
                    else:
                        id = count_files(datadir + "/id/") + 1
                        write_file(path, id)
                        path = datadir + "/about/" + str(id) + "/about.txt"
                        print(path)
                        content = "1\n100"
                        write_file(path, content)
                        Answer = to_num(user + "/" + str(id))


                elif code == "102":
                    # 認証
                    if value.project_client[gi] == "tw":
                        print("認証")
                        if tw_認証.get(str(user)) == 1:
                            Answer = user + to_num("/1")
                            print (1)
                            del tw_認証[str(user)]
                            print (0)

                elif code == "103":
                    print("認証")
                    if value.project_client[gi] == "sc":
                        tw_認証[str(user)] = 1
                        Answer = to_num(user + "/-1")
                    else:
                        Answer = to_num(user + "/-1")

            elif code == "110":
                path = datadir + "/about/" + str(id) + "password.txt"
                password = read_file(path)
                aad = pad_right(len(user), 4)
                nonce = pad_right(days_since_2000(), 24)
                if file_exists(path):
                    Answer = to_num(user + "/$$-0")
                    return Answer
                passvar = crpt.decrypt_data(password, req, nonce, aad)
                if password == passvar:
                    print("パスワードが一致しました")
                    sessionid = os.urandom(16).hex()
                    all_sessionid = read_file_lines(datadir + "/sessionid/all_ids.txt")
                    while sessionid in all_sessionid:
                        sessionid = os.urandom(16).hex()
                    all_sessionid.append(str(sessionid))
                    write_file(datadir + "/sessionid/all_ids.txt", all_sessionid)
                    write_file(datadir + "/sessionid/all_users.txt", user)
                    Answer = to_num(user + "/1/" + str(sessionid))
                else:
                    print("パスワードが間違っています")
                    Answer = to_num(user + "/$$-1")

                         
        elif code[0] == "2":
            # have id
            print("have id")
            id = str(user)
            # 未実装
            if code[2] == "0":
                print("get status")
                path = datadir + "/about/" + id + "/about.txt"
                file = str(read_file_lines(path)[0])
                if file == None:
                    Answer = to_num(id + "/-0")
                else:
                    Answer = to_num(id + "/" + file)
                        
            elif code[2] == "1":
                print("get point")
                path = datadir + "/about/" + id + "/about.txt"
                file = str(read_file_lines(path)[1])
                if file == None:
                    Answer = to_num(id + "/-0")
                else:
                    Answer = to_num(id + "/" + file)
            elif code[2] == "2":
                # TO DO
                print("TO DO")


        elif code[0] == "3":
            print ("global file")
            if code[2] == "0":
                print("look file")

                # 未実装

            elif code[2] == "1":
                print("== file ? (bool)")

                # 未実装
            elif code[2] == "2":
                print("count files")
                path = datadir + ""
                Answer = id + to_num( "/" + sum(os.path.isfile(os.path.join(path, name)) for name in os.listdir(path)) )
                # 未実装

            elif code[2] == "3":
                print("list files")

                # 未実装


                
        elif code[0] == "4":
            print("projects file")
            if code[2] == "0":
                print("look file")

                # 未実装

            elif code[2] == "1":
                print("== file ? (bool)")

                # 未実装
                
        elif code[0] == "5":
            if code[2] == "0":
                print ("mkdir")

                # 未実装
                    
            elif code[2] == "1":
                print("to do")

        elif code[0] == "6":
            print("point")
            if code[2] == "0":
                print("get log-in point")
                if value.project_privilege[gi] != "high":
                    print("Error: projectに十分な権限がありません")
                    Answer = to_num(user + "/-1")
                    print(Answer)
                    return Answer
                try:
                    f = open(datadir + "/about/" + to_txt(id) + "/login.txt", "r")
                    logintime = float(f.readline())
                    f.close()
                except Exception as error:
                    print(error)
                    try:
                        print("新規作成")
                        logintime = 0.0
                        file = open(datadir + "/about/" + to_txt(id) + "/login.txt", "x")
                        file.write("0")
                        file.close()
                    except FileExistsError:
                        print("fileの内容を修正")
                        file = open(datadir + "/about/" + to_txt(id) + "/login.txt", "w")
                        file.write("0")
                        file.close()

                if time.time()/86400 - logintime >= 1.0:
                    print("ログインポイントを更新")
                    path = datadir + "/about/" + to_txt(id) + "/about.txt"
                    file = read_file_lines(path)[1]
                    Answer = id + to_num("/" + str(float(file) + 3.0))

                    f = open(path, "w")
                    f.write(str(file[0].rstrip()) + "\n" + str(float(file) + 3.0) )
                    f.close

                    print("上書き")
                    file = open(datadir + "/about/" + to_txt(id) + "/login.txt", "w")
                    file.write(str(time.time()/86400))
                    file.close()
                else:
                    Answer = id + to_num("/" + "-1")
        print(Answer)
        return Answer

def purse_request(request):
    if request[0:2] == "11":
        return str(request[2:]), False
    elif request[0:2] == "10":
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
        if serverid != value.username:
            return 0
        return str(request[0:i]), True


def set_cloud (n,num:int, gi):
    conn = session.connect_cloud(value.project_id[gi])
    if value.project_client[gi] == "sc":
        conn = session.connect_cloud(value.project_id[gi])
    elif value.project_client[gi] == "tw":
        msg ="SCS project server by" + value.username + " on Scratch"
        conn = scratch3.get_tw_cloud(value.project_id[gi], contact=msg)
    conn.set_var(n,int(num))


def count_files(path):
    # ディレクトリ内のファイルをカウントする
    try:
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return len(files)
    except FileNotFoundError:
        print("指定したパスが見つかりません。")
        return 0

def write_file(path, txt):
    # 指定したパスにテキストファイルを作成して内容を書き込む
    txt = str(txt)
    # ディレクトリが存在しない場合は作成する
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, 'w') as file:
            file.write(txt)
        print(f"{path} にファイルを作成")
    except Exception as e:
        print(f"Error: {e}")

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
        print(f"{path} は見つかりませんでした。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

def read_file_lines(file_path):
    try:
        with open(file_path, 'r') as file:  # 'r'モードで読み込み
            lines = file.readlines()  # 各行をリストとして読む
        return lines
    except FileNotFoundError:
        print(f"{file_path} は見つかりませんでした。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

def file_exists(path):
  return os.path.exists(path)

def days_since_2000():
    # 2000年1月1日午前0時0分0秒をUTCで定義
    start_date = datetime(2000, 1, 1, 0, 0, 0)
    
    # 現在のUTC時間を取得
    current_date = datetime.utcnow()
    
    # 経過日数を計算
    delta = current_date - start_date
    return delta.days

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