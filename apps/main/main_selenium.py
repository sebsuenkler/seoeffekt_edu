#sub processes to start the Google selenium scraper

#include libs
import sys
sys.path.insert(0, '..')
from include import *



def google_selenium():
    call(["python3", "proc_google_selenium.py"])


process5 = threading.Thread(target=google_selenium)


process5.start()
