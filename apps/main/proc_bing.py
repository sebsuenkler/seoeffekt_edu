#sub processes to scrape bing

#include libs
import sys
sys.path.insert(0, '..')
from include import *

def bing_api():
    call(["python3", "job_bing_api.py"])

process1 = threading.Thread(target=bing_api)

process1.start()
