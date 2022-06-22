import sqlite3 as sl

connection = sl.connect('seo_effect.db')

cursor=connection.cursor()

with connection:
    data = cursor.execute("SELECT * FROM SCRAPER WHERE progress =? ORDER BY RANDOM() LIMIT 1", (0,))
    for row in data:
        id = row[0]
        query = row[3]
        search_engine = row[4]


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time

import json

with open('scraper.json') as json_file:
    search_engines_json = json.load(json_file)

search_box = search_engines_json[search_engine]['search-box']
max_number_pages = search_engines_json[search_engine]['max_number_pages']
search_url = search_engines_json[search_engine]['search_url']
xpath_results = search_engines_json[search_engine]['xpath_results']
xpath_next_page = search_engines_json[search_engine]['xpath_next_page']
max_results_filter = search_engines_json[search_engine]['max_results_filter']
captcha = search_engines_json[search_engine]['captcha']

pages = []


import os
current_path = os.path.abspath(os.getcwd())

if os.name == "nt":
    extension_path = current_path+"\i_dont_care_about_cookies-3.4.0.xpi"

else:
    extension_path = current_path+"/i_dont_care_about_cookies-3.4.0.xpi"

options = Options()
options.headless = False

driver = webdriver.Firefox(options=options)
driver.install_addon(extension_path, temporary=False)
driver.get(search_url)
time.sleep(3)
search = driver.find_element(By.NAME, search_box)
search.send_keys(query)
search.send_keys(Keys.RETURN)
time.sleep(3)

init_page = 2

x = range(init_page, init_page+max_number_pages)

for n in x:
    r = str(n)
    page = 'Page '+r
    pages.append(page)

for p in pages:

    paging = driver.find_element(By.XPATH, xpath_next_page.format(p))

    paging.click()

    time.sleep(3)


driver.quit()
