#processing libraries
import threading
import importlib
from subprocess import call
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

def source():
    call(["python", "job_source.py"])

def scraper():
    call(["python", "job_scraper.py"])

def reset_scraper():
    call(["python", "job_reset_scraper.py"])

def classifier():
    call(["python", "job_classifier.py"])

process1 = threading.Thread(target=source)
process2 = threading.Thread(target=scraper)
process3 = threading.Thread(target=reset_scraper)
process4 = threading.Thread(target=classifier)

process1.start()
process2.start()
process3.start()
process4.start()
