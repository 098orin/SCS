# this project is using https://github.com/TimMcCool/scratchattach

# main.py

# import value
import time
import fun

"""
try:
    import scratchattach as scratch3
except:
    import os
    os.system("pip install -U scratchattach")
    import scratchattach as scratch3
"""

from datetime import datetime

def days_since_2000():
    # 2000年1月1日午前0時0分0秒をUTCで定義
    start_date = datetime(2000, 1, 1, 0, 0, 0)
    
    # 現在のUTC時間を取得
    current_date = datetime.utcnow()
    
    # 経過日数を計算
    delta = current_date - start_date
    return delta.days

def main(id, i):
    # session = scratch3.login(value.username, value.password)
    # conn = session.connect_cloud(id)

    fun.set_cloud("time", days_since_2000(), i) #the variable name is specified without the cloud emoji
    print(id)
    fun.response_cloudvalues (fun.getcloudvalues(id, i) , id, i)