from email.policy import default
import value
import global_value as g
import json
import time
import os

try:
    import scratchattach as scratch3
except:
    os.system("pip install -U scratchattach")
    import scratchattach as scratch3

global i2

pdata = {}

session = scratch3.login(value.username, value.password)

# datadir = os.path.expanduser ("~").replace(os.sep,'/') + "/SCS_data"
datadir = value.datadir

tw_認証 = dict()
watting = list()

def to_txt(number):
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


def getcloudvalues(id):
    if value.project_client[g.i2] == "sc":
        request = scratch3.get_cloud(id) #Returns a dict with all cloud var values
        del request['time']
    elif value.project_client[g.i2] == "tw":
        request = scratch3.get_tw_cloud(id)
        TS1 = "{"
        for i in range(len(request)):
            TS = request[i]
            if TS["name"] != "☁ time":
                TS = '"' + str( TS["name"] )[2] + '": "' + str(TS["value"])  + '"'
                if i != len(request) - 1:
                    TS = TS + ", "
                TS1 = TS1 + TS
        TS1 = TS1 + "}"
        request = json.loads(TS1)
    
    return request

def responscloudvalues (repuest,id):
    print(repuest)
    if repuest:
        for n in list(repuest):
            n = str(n)
            if str(repuest[n]) != "60353425": #not None
                req = to_txt ( repuest[n])
                user = to_txt ( repuest[n][10:len(repuest[n])-2] )
                Answer = ""
                code = str(to_txt(repuest[n][2:8]))
                for i in range(len(req)):
                    if req[i] == "/":
                        server_id = Answer
                        Answer = ""
                        break
                    else:
                        if i >= 2:
                            Answer = Answer + req[i]
                
                if server_id != value.username and server_id != "all":
                    print("400 Bad request")
                    print("サーバー管理者の方は`value.py`に適切なproject id を設定しているか確認してください。")
                    print("project id が正しい場合、プロジェクトに不備がある可能性があります。")
                    print("プロジェクト側の@server_idが正しく自分の`value.py`のusernameと一致していることを確認してください。")
                    print("===")
                    Answer =str(user) + to_num("/" + "-1")
                    print(Answer)
                    print(to_txt(Answer))
                    set_cloud(str(n), Answer)
                


                if code[0] != "1":
                    id = repuest[n][10:len(repuest[n])-2]

                if str(to_txt(repuest[n][0:2])) == "#":
                    #have datas
                    datas = ["","","","","","",]
                    i1 = 0
                    data = ""
                    for i in range(len(req)-8):
                        i = i + 5
                        if "/" == req[i]:
                            if i1 == 0:
                                if code[0] != 1:
                                    id = data
                                else:
                                    user = data
                            else:
                                datas[i1-1] = data
                            i1 = i1 + 1
                            data = ""
                        data = data + str(req[i])

                if code[0] == "1":
                    # no id
                    print('no id')
                    if code[2] == "0":
                        path = datadir + "/id/" + str(user) + ".txt"
                        print(path)
                        if os.path.isfile(path):
                            with open(path) as file:
                                file = file.read()
                                print(file)
                                # <class '_io.TextIOWrapper'>
                        else:
                            file = "0"
                        Answer =str(user) + to_num("/" + str(file))
                        print(Answer)
                        print(to_txt(Answer))
                        set_cloud(str(n), Answer)

                    elif code[2] == "1":
                        # make id
                        if value.project_privilege[g.i2] != "high":
                            continue
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
                        if not os.path.exists(os.path.dirname(path)):
                            os.makedirs(os.path.dirname(path))
                        print(path)
                        if not os.path.isfile(path):
                            with open(path, mode='w', newline="\n") as file:
                                file.write( "1\n" + "100" )
                            Answer = str(user) + to_num("/")
                        set_cloud(str(n), Answer)
                        print(Answer)
                    elif code[2] == "2":
                        Answer = user + to_num("/0")
                        if value.project_client[g.i2] == "tw":
                            print("認証")
                            if tw_認証.get(str(user)) == 1:
                                Answer = user + to_num("/1")
                                print (1)
                                del tw_認証[str(user)]
                                print (0)
                        set_cloud(str(n), Answer)

                    elif code[2] == "3":
                        print("認証")
                        if value.project_client[g.i2] == "sc":
                            tw_認証[str(user)] = 1
                        Answer = user + to_num("/0")
                        set_cloud(str(n), Answer)
                            
                elif code[0] == "2":
                    # have id
                    print("have id")
                    id = repuest[n][10:len(repuest[n])-2]
                    if code[2] == "0":
                        path = datadir + "/about/" + to_txt(id) + "/about.txt"
                        with open(path, mode='r', newline='\n') as file:
                            file = file.readlines()
                            file = file[0].rstrip()  # 1行目を取得
                        print(file)
                        Answer = id + to_num("/" + str(file))
                        print(Answer)
                        set_cloud(str(n), Answer)
                        
                    elif code[2] == "1":
                        path = datadir + "/about/" + to_txt(id) + "/about.txt"
                        with open(path, mode='r', newline='\n') as file:
                            file = file.readlines()
                            file = file[1].rstrip()  # 2行目を取得
                        print(file)
                        Answer = id + to_num("/" + str(file))
                        print(Answer)
                        set_cloud(str(n), Answer)
                    elif code[2] == "2":
                        # TO DO
                        print("TO DO")

                elif code[0] == "3":
                    print ("global file")
                    if code[2] == "0":
                        print("look file")
                        path = datadir + "/global/" + datas[0]
                        with open(path, mode="r", newline='\n') as file:
                            file = file.readlines()
                        Answer = id + to_num("/" + str(file))
                        set_cloud(str(n), Answer)

                    elif code[2] == "1":
                        print("== file ? (bool)")
                        path = datadir + "/global/" + datas[0]
                        with open(path, mode="r", newline='\n') as file:
                            file = file.readlines()
                        if datas[1] == str(file):
                            Answer = id + to_num("/" + 1)
                        else:
                            Answer = id + to_num("/" + 0)
                        set_cloud(str(n), Answer)

                    elif code[2] == "2":
                        print("count files")
                        path = datadir + data[0]
                        Answer = id + to_num( "/" + sum(os.path.isfile(os.path.join(path, name)) for name in os.listdir(path)) )
                        set_cloud(str(n), Answer)

                    elif code[2] == "3":
                        print("list files")


                
                elif code[0] == "4":
                    print("projects file")
                    if code[2] == "0":
                        print("look file")
                        path = datadir + "/projects/" + datas[0]
                        with open(path, mode="r", newline='\n') as file:
                            file = file.readlines()
                        Answer = id + to_num("/" + str(file))
                        set_cloud(str(n), Answer)

                    elif code[2] == "1":
                        print("== file ? (bool)")
                        path = datadir + "/projects/" + datas[0]
                        with open(path, mode="r", newline='\n') as file:
                            file = file.readlines()
                        if datas[1] == str(file):
                            Answer = str(id) + to_num("/" + 1)
                        else:
                            Answer = str(id) + to_num("/" + 0)
                        set_cloud(str(n), Answer)
                
                elif code[0] == "5":
                    if code[2] == "0":
                        print ("mkdir")
                    
                    elif code[2] == "1":
                        print("to do")

                elif code[0] == "6":
                    print("point")
                    if code[2] == "0":
                        print("get log-in point")
                        if value.project_privilege[g.i2] != "high":
                            continue
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
                            with open(path, mode='r', newline='\n') as file:
                                file = file.readlines()
                                print(file)
                                file2 = file[1].rstrip()  # 2行目を取得
                            print(file2)
                            Answer = id + to_num("/" + str(float(file2) + 3.0))

                            f = open(path, "w")
                            f.write(str(file[0].rstrip()) + "\n" + str(float(file2) + 3.0) )
                            f.close

                            print("上書き")
                            file = open(datadir + "/about/" + to_txt(id) + "/login.txt", "w")
                            file.write(str(time.time()/86400))
                            file.close()
                        else:
                            Answer = id + to_num("/" + "-1")

                        print(Answer)
                        set_cloud(str(n), Answer)
                            



def set_cloud (n,num:int):
    conn = session.connect_cloud(value.project_id[g.i2])
    if value.project_client[g.i2] == "sc":
        conn = session.connect_cloud(value.project_id[g.i2])
    elif value.project_client[g.i2] == "tw":
        msg ="SCS project server by" + value.username + " on Scratch"
        conn = session.connect_tw_cloud(value.project_id[g.i2], contact=msg)
    conn.set_var(n,int(num))


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