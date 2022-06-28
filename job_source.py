#processing libraries
import threading
import importlib
from subprocess import call
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import os
import time


job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

def job():
    os.system('python source.py')

if __name__ == '__main__':
    scheduler = BackgroundScheduler(job_defaults=job_defaults, timezone='Europe/Berlin')
    scheduler.add_job(job, 'interval', seconds=60)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    print('source_job')

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
