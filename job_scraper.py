#processing libraries
import threading
import importlib
from subprocess import call
from apscheduler.schedulers.background import BackgroundScheduler
import os
import time
import datetime

def write_to_log(timestamp, content):
    f = open("main.log", "a+")
    f.write(timestamp+": "+content+"\n")
    f.close()

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

def job():
    os.system('python scraper.py')

if __name__ == '__main__':
    scheduler = BackgroundScheduler(job_defaults=job_defaults, timezone='Europe/Berlin')
    scheduler.add_job(job, 'interval', seconds=60, next_run_time=datetime.datetime.now())
    scheduler.start()

    time.sleep(1)

    timestamp = datetime.datetime.now()
    timestamp = timestamp.strftime("%d-%m-%Y, %H:%M:%S")

    write_to_log(timestamp, "Job_Scraper started")

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
