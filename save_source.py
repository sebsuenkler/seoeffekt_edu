from selenium import webdriver

import time

driver = webdriver.Firefox()
driver.install_addon(r"./extensions/i_dont_care_about_cookies-3.4.0.xpi", temporary=False)
driver.get("https:/spiegel.de")
time.sleep(10)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(10)
source = driver.page_source

driver.quit()
