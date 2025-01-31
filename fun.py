# from email.policy import default
import value
# import global_value as g
import json
import time
import os
from datetime import datetime

try:
    import scratchattach as scratch3
except:
    os.system("pip install -U scratchattach")
    import scratchattach as scratch3
print(os.system("pip show scratchattach"))

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
        """
        TS1 = "{"
        for i in range(len(request)):
            TS = request[i]
            if TS["name"] != "☁ time":
                TS = '"' + str( TS["name"] )[2] + '": "' + str(TS["value"])  + '"'
                if i != len(request) - 1:
                    TS = TS + ", "
                TS1 = TS1 + TS
        TS1 = TS1 + "}"
        """
        # request = json.loads(request)
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
    request = str(request)
    if request != "0": #not None
        code = request[0:3]
        req = to_txt(request[3:len(request)])

        user = ""
        for i in range(len(req)):
            if req[i] == "/":
                break
            user = user + req[i]
        
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
                    path = datadir + "/id/" + str(user) + ".txt"
                    id = read_file(path)
                    if id == None:
                        pass

                elif code[2] == "1":
                    # make id
                    print ("make id") 
                    if value.project_privilege[gi] != "high":
                        print("Error: projectに十分な権限がありません")
                        Answer = to_num(user + "/-1")
                        print(Answer)
                        return Answer
                    path = datadir + "/id/" + str(user) + ".txt"
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


                elif code[2] == "2":
                    # 認証
                    if value.project_client[gi] == "tw":
                        print("認証")
                        if tw_認証.get(str(user)) == 1:
                            Answer = user + to_num("/1")
                            print (1)
                            del tw_認証[str(user)]
                            print (0)

                elif code[2] == "3":
                    print("認証")
                    if value.project_client[gi] == "sc":
                        tw_認証[str(user)] = 1
                        Answer = to_num(user + "/-1")
                    else:
                        Answer = to_num(user + "/-1")

            elif code[1] == "1":
                if code[2] == "0":
                    path = datadir + "/about/password.txt"
                    password = read_file(path)
                    passvar = unlock(password,days_since_2000(),var)
                    if password == passvar:
                        print("パスワードが一致しました")
                        Answer = user + to_num("/1")
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


def set_cloud (n,num:int, gi):
    conn = session.connect_cloud(value.project_id[gi])
    if value.project_client[gi] == "sc":
        conn = session.connect_cloud(value.project_id[gi])
    elif value.project_client[gi] == "tw":
        msg ="SCS project server by" + value.username + " on Scratch"
        conn = scratch3.get_tw_cloud(value.project_id[gi], contact=msg)
    conn.set_var(n,int(num))

def lock(key,IV,data,b=0):
    if len(str(key)) < 11:
        return lock(str(key) + "0",IV,data,b)
    if b != 5:
        return lock(base(key,5),IV,base(data,5),5)
    Answer = ""
    sBox = s_box(data,key)
    i = j = 0
    for k in range(len(data)):
        i = (i+1) % len(sBox)
        j = (j + sBox[i]) % len(sBox)
        if str(data[k]) == str(sBox[j]):
            Answer = Answer + "0"
        else:
            Answer = Answer + str(int(data[k]) + int(sBox[j]))
    i = ""
    k = 0
    for j in list(Answer):
        k += 1
        if k == 1:
            i = 1 + int(j)
        else:
            i = str(i) + str(j)
    Answer = int(i)
    Answer = Answer * IV + IV
    sBox = s_box(Answer, str(IV)+str(key), IV=True)
    Answer = "1"
    for i in sBox:
        Answer = Answer + str(i)
    return Answer

def unlock(key,IV, data,b=0):
    if len(str(key)) < 11:
        return unlock(str(key) + "0",IV,data,b)
    if b != 5:
        sBox = s_box(data[1:],str(IV)+base(key,5),IV=True,unlock=True)
        Answer = str("".join(map(str,sBox)))
        Answer = int(Answer) - int(str(IV) + str(base(key,5)))
        Answer = str((Answer - IV) // IV)
        k = 0
        i = ""
        for k in range(len(Answer)):
            if k == 0:
                i = int(Answer[0]) - 1
            else:
                i = str(i) + Answer[k]
        return unlock(base(key,5),IV,i,5)
    sBox = s_box(data,key)
    i = j = k = 0
    Answer = ""
    data = str(data)
    for k in range(len(data)):
        i = (i+1) % len(sBox)
        j = (j + int(sBox[i])) % len(sBox)
        if "0" == str(sBox[j]):
            Answer = Answer + str(sBox[j])
        else:
            Answer = Answer + str(int(data[k]) - int(sBox[j]))
    return str(int(Answer,5))

def s_box(data,key,IV=False,unlock=False):
    sBox = list() 
    if unlock:
        for i in data:
            sBox.append(i)
    elif IV:
        for i in str(int(data)+int(key)):
            sBox.append(i)
    else:
        for i in range(len(str(data))):
            sBox.append(i%6)

    data = str(data)
    key = str(key)
    if unlock:
        for i in range(len(sBox)):
            i2 = len(sBox) - i -1
            j = (i2 + int(key[i2%len(key)])) %len(sBox)
            sBox[i2], sBox[j] = sBox[j], sBox[i2]
    else:
        for i in range(len(sBox)):
            j = (i + int(key[i % len(key)])) % len(sBox)
            sBox[i], sBox[j] = sBox[j], sBox[i]

    return sBox
        

def base(num, base):
    num = int(num)
    if num == 0:
        return "0"
    
    digits = ""
    while num > 0:
        remainder = num % base
        if remainder < 10:
            digits = str(remainder) + digits  # 0-9の場合
        else:
            digits = chr(remainder - 10 + ord('A')) + digits  # 10-15の場合（16進数用）
        num //= base

    return digits

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

def days_since_2000():
    # 2000年1月1日午前0時0分0秒をUTCで定義
    start_date = datetime(2000, 1, 1, 0, 0, 0)
    
    # 現在のUTC時間を取得
    current_date = datetime.utcnow()
    
    # 経過日数を計算
    delta = current_date - start_date
    return delta.days
