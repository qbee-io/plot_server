import requests
import datetime
from time import sleep
import math
from random import gauss
import psutil
import re
import os


host = 'localhost'
port = 8080
url = f"http://{host}:{port}"

sampling_rate = 2000 #in milliseconds
noise = 0.1
freq = 0.5
amp = 2
base = 20

tag = "Temperature - Room1"
unit = "\u2103" #degree celsius

offset = datetime.datetime.now().replace(
            minute=0, second=0, microsecond=0
        ).timestamp()

#restart if already running
for process in psutil.process_iter():
    has_file = sum([1 for x in process.cmdline() if re.search(__file__,x)])
    if has_file and process.pid != os.getpid():
        print("killing process: ", process.cmdline())
        try:
            process.terminate()
        except psutil.AccessDenied:
            print("access denied ... continuing")

while(True):
    now = datetime.datetime.now().timestamp()
    val = base + amp*math.sin(freq*(now-offset)) + gauss(0,noise)
    data = {
        'tag': tag,
        'value': val,
        'ts': now,
        'unit': unit
    }
    try:
        requests.post(url,json=data)
    except:
        print("server cannot be reached")
    print(val)
    sleep(sampling_rate/1000)

