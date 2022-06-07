#sub processes to scrape Google selenium

#include libs
import sys
sys.path.insert(0, '..')
from include import *

def google_selenium():
    call(["python3", "job_google_selenium.py"])

def google_selenium_sv():
    call(["python3", "job_google_selenium_sv.py"])

def reset_scraper():
    call(["python3", "job_reset_scraper.py"])

process1 = threading.Thread(target=google_selenium)
process2 = threading.Thread(target=reset_scraper)
process3 = threading.Thread(target=google_selenium_sv)

process1.start()
process2.start()
process3.start()
