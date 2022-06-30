import sqlite3 as sl
from lib.sources import save_source
import threading
import importlib
from subprocess import call
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import threading
import importlib
from subprocess import call
from apscheduler.schedulers.background import BackgroundScheduler
import os
import time
import datetime
import csv
import json
from datetime import date
import pandas as pd
import base64
from datetime import date

from lib.sources import *


today = date.today()

from urllib.parse import urlsplit
from urllib.parse import urlparse
import socket

from lxml import html
from bs4 import BeautifulSoup
import fnmatch

from lib.identify_indicators import *

import sqlite3 as sl

import datetime

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True

import os
current_path = os.path.abspath(os.getcwd())

if os.name == "nt":
    extension_path = current_path+"\i_dont_care_about_cookies-3.4.0.xpi"

else:
    extension_path = current_path+"/i_dont_care_about_cookies-3.4.0.xpi"

url = "https://www.spiegel.de/"

driver = webdriver.Firefox(options=options)
driver.install_addon(extension_path, temporary=False)
driver.set_page_load_timeout(120)
try:
    driver.get(url)
    time.sleep(10)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    source = driver.page_source
    source = encode_source(source)
    source_decoded = decode_source(source)

except:
    source = "error"


driver.quit()


f = open("test_source.txt", "w+", encoding='utf-8')
f.write(str(source))
f.close()

f = open("test_source_dec.html", "w+", encoding='utf-8')
f.write(str(source_decoded))
f.close()

import fnmatch
from urllib.parse import urlparse
import csv
import json
from lxml import html
from bs4 import BeautifulSoup

from lib.sources import save_robot_txt
from lib.sources import calculate_loading_time
