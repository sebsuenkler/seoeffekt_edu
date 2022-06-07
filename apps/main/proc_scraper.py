#sub processes to scrape using the normal Google scraper

#include libs
import sys
sys.path.insert(0, '..')
from include import *

def save_sources():
    call(["python3", "job_save_sources.py"])

def scraper():
    call(["python3", "job_scraper.py"])

def reset_scraper():
    call(["python3", "job_reset_scraper.py"])

def reset_sources():
    call(["python3", "job_reset_sources.py"])

process1 = threading.Thread(target=scraper)
process2 = threading.Thread(target=save_sources)
process3 = threading.Thread(target=reset_scraper)
process4 = threading.Thread(target=reset_sources)

process1.start()
process2.start()
process3.start()
process4.start()
