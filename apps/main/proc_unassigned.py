#sub processes to delete unassigned results

#include libs
import sys
sys.path.insert(0, '..')
from include import *

def speed():
    call(["python3", "job_unassigned.py"])

process1 = threading.Thread(target=speed)

process1.start()
