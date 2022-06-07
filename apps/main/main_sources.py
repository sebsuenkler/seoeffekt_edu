#sub processes to save html source codes and to measure the loading speed of a webpage

#include libs
import sys
sys.path.insert(0, '..')
from include import *



def speed():
    call(["python3", "proc_speed.py"])

def sources():
    call(["python3", "proc_scraper.py"])



process5 = threading.Thread(target=speed)

process6 = threading.Thread(target=sources)

process5.start()

process6.start()
