# from email.policy import default
import value
# import global_value as g
import json
import time
import os

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
        txt = "/#0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_+.\\"
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
    txt = "/#0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_+.\\"
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

def response_cloudvalues (repuest,id, gi):
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

def lock_txt(txt,password):
    s_box = _s_box(password)
    for i in range(32):
        i += 1
        i1 = i % (len(txt) + 1)
        i1 = txt[i1]
        i -= 1
        if s_box[i] == i1:
            s_box[i] = "00"
        else:
            s_box[i] = str(s_box[i] + i1)
        if len(s_box[i]) == 1:
            s_box.insert(i,"0" + str(s_box[i]) )
    Answer = ""
    for i in range(32):
        Answer = Answer + str(s_box[i])


def _s_box(password):
    s_box = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
    for i in range(64):
        i += 1
        i1 = i % len(password) + 1
        i1 = i + password[i1]
        i1 = i1 % len(password)
        i -= 1
        if i != i1:
            s_box.insert(i, s_box[i])
            if i1 <= i:
                s_box.insert(i, s_box[i+1])
            else:
                s_box.insert(i1+1, s_box[i+1])
        del s_box[i+1]
        del s_box[i1+1]
    return s_box