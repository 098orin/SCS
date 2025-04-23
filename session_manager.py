import fun
import time
import value

datadir = value.datadir

while True:
    try:
        delindex = []
        all_sessiontimestamp = fun.read_file_lines(datadir + "session/all_timestamps.txt")
        date = fun.days_since_2000()
        for i in range(all_sessiontimestamp):
            if date-i >= 1:
                 index = all_sessiontimestamp.index(i)
                 delindex.append(index)
        if len(delindex) != 0:
            all_sessionid = fun.read_file_lines(datadir + "session/all_ids.txt")
            all_sessionuser = fun.read_file_lines(datadir + "session/all_users.txt")
            delindex.sort(reverse=True)
            for i in delindex:
                all_sessionid.pop(i)
                all_sessionuser.pop(i)
                all_sessiontimestamp.pop(i)
            fun.write_file(datadir + "session/all_ids.txt", all_sessionid)
            fun.write_file(datadir + "session/all_users.txt", all_sessionuser)
            fun.write_file(datadir + "session/all_timestamps.txt", all_sessiontimestamp)
    except Exception as e:
        print("While checking session error occurred.")
        print(f"Error: {e}")
    time.sleep(180)