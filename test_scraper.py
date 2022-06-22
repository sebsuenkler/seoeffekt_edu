from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

import time

search_query = "merkel"

pages = []

driver = webdriver.Firefox()
driver.install_addon(r"./extensions/i_dont_care_about_cookies-3.4.0.xpi", temporary=False)
driver.get("https:/google.com")
time.sleep(3)
search = driver.find_element(By.NAME, "q")
search.send_keys(search_query)
search.send_keys(Keys.RETURN)
time.sleep(3)

number_pages = 4

x = range(2, number_pages)

for n in x:
    r = str(n)
    page = 'Page '+r
    pages.append(page)


for p in pages:

    paging = driver.find_element(By.XPATH, "//a[@aria-label='{}']".format(p))

    paging.click()

    time.sleep(3)


driver.quit()
