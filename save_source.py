from selenium import webdriver

import time

import os
current_path = os.path.abspath(os.getcwd())

if os.name == "nt":
    extension_path = current_path+"\i_dont_care_about_cookies-3.4.0.xpi"

else:
    extension_path = current_path+"/i_dont_care_about_cookies-3.4.0.xpi"


driver = webdriver.Firefox()
driver.install_addon(extension_path, temporary=False)
try:
    driver.get("https:/stahlschlag.de")
    time.sleep(10)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    source = driver.page_source
except:
    source = "error"

driver.quit()

source = source.encode('utf-8')

with open('source_test.txt', 'w+') as f:
    f.write(str(source))
