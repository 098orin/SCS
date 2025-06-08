import sys
import signal
from datetime import datetime, timedelta
import threading
import scratchattach as scratch3
import value
import fun

gi = int(sys.argv[1])
if value.project_client[gi] == "sc":
    session = scratch3.login(value.username, value.password) # Log in to Scratch
    cloud = session.connect_scratch_cloud(value.project_id[gi]) # Connect Scratch's cloud
    events = cloud.events()
elif value.project_client[gi] == "tw":
    cloud = scratch3.get_tw_cloud(value.project_id[gi])
    events = cloud.events()

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
        print(f"{gi}:Error: {str(error)}")

nonces = dict() # Nonce dictionary to store nonces for each user
clouds = dict() # Dictionary to store cloud variables
"""
This is a dictionary to store nonces for each user.
The key is the username and the value is a list of fixed_IV, sequense_number.
"""

@events.event
def on_set(activity): #Called when a cloud var is set
    global nonces
    if value.project_client[gi] == "sc":
        activity.load_log_data()
        print(f"{activity.username} set variable {activity.var} to {activity.value} at {activity.timestamp}")
        username = activity.username
        if activity.username == value.username:
            return # Ignore own changes
    elif value.project_client[gi] == "tw":
        print(f"variable {activity.var} was set to {activity.value} at {activity.timestamp}")
        username = None
    response, nonces = fun.response(activity.value, gi, nonces, username=username)
    print(f"Response: {response}")
    set_cloud(activity.var, response, gi)
    # To get the user who set the variable, call activity.load_log_data() which saves the username to the activity.username attribute

@events.event
def on_del(activity):
    print(f"{activity.user} deleted variable {activity.var}")

@events.event
def on_create(activity):
    print(f"{activity.user} created variable {activity.var}")

@events.event #Called when the event listener is ready
def on_ready():
   print(f"{gi}: Event listener ready!")

def sigterm_handler(signum, frame):
    fun.cleanup()  # ログファイルを閉じる


signal.signal(signal.SIGTERM, sigterm_handler)
events.start()

def cloud_timeout_manager():
    """
    This function is used to manage the cloud timeout.
    """
    logs = cloud.logs()
    timeouted_vars = {}
    for log in logs:
        if log.type == "set":
            if log.timestamp < datetime.utcnow()-timedelta(seconds=60) and log.varlue != 0:
                timeouted_vars[log.var] = 0
    if len(timeouted_vars) > 0:
        cloud.set_vars(timeouted_vars)
    timer = threading.Timer(120.0, cloud_timeout_manager)
    timer.start()  # 120秒ごとにタイムアウトを確認

if value.project_client[gi] == "sc":
    timer = threading.Timer(120.0, cloud_timeout_manager)
    timer.start()  # 120秒ごとにタイムアウトを確認
    print(f"{gi}: Cloud timeout manager started.")

