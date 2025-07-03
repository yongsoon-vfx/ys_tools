import os
import time

stime = round(time.time(), 2)
os.environ["_stime"] = str(stime)
