import os

print("Server version: v.1.2.1")

if os.geteuid() == 0:
    print("管理者権限で実行中です")
else:
    print("非管理者権限で実行中です")




import main
import value
import global_value as g
# import time


path = value.path

file = open(path + "/fun.py", "br")
fun_hash_old = hash(file.read())
file.close()

file = open(path + "/value.py", "br")
val_hash_old = hash(file.read())
file.close()

i = 1
while True:
    i += 1
    for g.i2 in range(len(value.project_id)):
        try:
            main.main(value.project_id[g.i2])
        except Exception as error:
            print(error)
        # time.sleep(0.05)


    if 1 == 50:
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
    