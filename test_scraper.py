from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.firefox.options import Options

import time

import os
current_path = os.path.abspath(os.getcwd())

if os.name == "nt":
    extension_path = current_path+"\i_dont_care_about_cookies-3.4.0.xpi"
else:
    extension_path = current_path+"/i_dont_care_about_cookies-3.4.0.xpi"

search_query = "merkel"

options = Options()
options.headless = True

pages = []

driver = webdriver.Firefox(options=options)
driver.install_addon(extension_path, temporary=False)
driver.get("https:/google.com")
time.sleep(3)
search = driver.find_element(By.NAME, "q")
search.send_keys(search_query)
search.send_keys(Keys.RETURN)
time.sleep(3)

number_pages = 4

x = range(2, number_pages)

source = driver.page_source
print(source)

for n in x:
    r = str(n)
    page = 'Page '+r
    pages.append(page)


for p in pages:

    paging = driver.find_element(By.XPATH, "//a[@aria-label='{}']".format(p))

    paging.click()

    time.sleep(3)

    source = driver.page_source
    print(source)


driver.quit()
