#sub processes to collect seo indicators and to classify the documents

#include libs
import sys
sys.path.insert(0, '..')
from include import *

def indicators():
    call(["python3", "job_indicators.py"])

def classifier():
    call(["python3", "job_classifier.py"])


process1 = threading.Thread(target=indicators)
process2 = threading.Thread(target=classifier)

process1.start()
process2.start()
