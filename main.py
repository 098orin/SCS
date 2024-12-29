# this project is using https://github.com/TimMcCool/scratchattach

# main.py

import value
import time
import fun

try:
    import scratchattach as scratch3
except:
    import os
    os.system("pip install -U scratchattach")
    import scratchattach as scratch3

def main(id):
    # session = scratch3.login(value.username, value.password)
    # conn = session.connect_cloud(id)
    
    unix_time = time.time() - 946652400.0
    unix_time = unix_time/3600/24
    unix_time = unix_time-1.0
    # print("Time stamp:", unix_time)
    fun.set_cloud("time", unix_time) #the variable name is specified without the cloud emoji
    print(id)
    fun.responscloudvalues (fun.getcloudvalues(id) , id)