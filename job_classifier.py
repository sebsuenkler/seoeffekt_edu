#processing libraries
import threading
import importlib
from subprocess import call
from apscheduler.schedulers.background import BackgroundScheduler
import os
import time
import datetime

from log import *

job_defaults = {
    'coalesce': False,
    'max_instances': 1
}

def job():
    os.system('python classifier.py')

if __name__ == '__main__':
    scheduler = BackgroundScheduler(job_defaults=job_defaults, timezone='Europe/Berlin')
    scheduler.add_job(job, 'interval', seconds=30, next_run_time=datetime.datetime.now())
    scheduler.start()

    time.sleep(4)

    timestamp = datetime.datetime.now()
    timestamp = timestamp.strftime("%d-%m-%Y, %H:%M:%S")

    write_to_log(timestamp, "Job_Classifier started")

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
