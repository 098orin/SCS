import time
import scratchattach as sa
import random
project_id = 1116728993
connection = sa.get_tw_cloud(project_id)
connection.connect()
while True:
    connection.set_var("変数", str(random.randint(0, 1000))+"1234567890")
    time.sleep(1)