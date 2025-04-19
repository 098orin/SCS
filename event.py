import sys
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

@events.event
def on_set(activity): #Called when a cloud var is set
    print(f"Variable {activity.var} was set to the value {activity.value} at {activity.timestamp}")
    response = fun.response(activity.value, gi)
    fun.set_cloud(activity.var, response, gi)
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

events.start()