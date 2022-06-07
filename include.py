#libraries for the app

#date libs
from datetime import date
from datetime import datetime
from datetime import timedelta
import datetime
import time

#scraping libs
from os.path import isfile, join
from lxml import html
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup, Comment
import lxml.html
import requests
requests.packages.urllib3.disable_warnings()
from urllib.request import urlparse, urljoin
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

#file libs
import json
import csv

# sys libs
import os
import os, sys
import os.path
sys.path.insert(0, '../..')

#db libs
from db.connect import DB
from libs.scrapers import Scrapers
from libs.queries import Queries
from libs.results import Results
from libs.studies import Studies
from libs.evaluations import Evaluations
from libs.helpers import Helpers
from libs.sources import Sources

#processing libraries
import threading
import importlib
from subprocess import call
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

#other libs
import re
import random

#ml libs
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate, StratifiedShuffleSplit
from sklearn.tree import DecisionTreeClassifier
from imblearn.over_sampling import RandomOverSampler

from joblib import load


#load global vars
with open('../../config/global_vars.ini', 'r') as f:
    array = json.load(f)

update = array['update']

today = date.today()

number_indicators = array['indicators']

if update == "0":
    def check_evaluations_result(hash, module, value):
        if (not Evaluations.getEvaluationModule(hash, module)):
            Evaluations.insertEvaluationResult(hash, module, value, today)
else:
    def check_evaluations_result(hash, module, value):
        if (not Evaluations.getEvaluationModule(hash, module)):
            Evaluations.insertEvaluationResult(hash, module, value, today)
        else:
            evaluations_date = Evaluations.getEvaluationsDate(hash, module)
            diff = today - evaluations_date[0][0]
            if diff.days > days:
                UpdateEvaluationResult(value, today, hash, module)
