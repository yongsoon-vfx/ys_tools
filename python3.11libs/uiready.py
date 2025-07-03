import os
import time

stime = float(os.getenv("_stime"))
ctime = round(time.time(), 2)
time_taken = round(ctime - stime, 2)
print(f"Time taken to load HDAs & GUI: {time_taken}s")
