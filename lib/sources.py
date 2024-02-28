from seleniumwire import webdriver

from selenium.webdriver.chrome.options import Options


import time

import os
current_path = os.path.abspath(os.getcwd())

import base64

from bs4 import BeautifulSoup

if os.name == "nt":
    extension_path = current_path+"\i_dont_care_about_cookies-3.4.0.xpi"

else:
    extension_path = current_path+"/i_dont_care_about_cookies-3.4.0.xpi"

options = Options()
desired_dpi = 1.0
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
options.add_argument('--no-sandbox')
options.add_argument("--start-maximized")
options.add_argument('--disable-dev-shm-usage')

#remove the comment if you want to scrape with the headless browser
#options.add_argument('--headless=new')


options.add_extension(extension_path)


def encode_source(source):
    source = source.encode('utf-8','ignore')
    source = base64.b64encode(source)
    return source

def decode_source(source):
    source_decoded = base64.b64decode(source)
    source_decoded = BeautifulSoup(source_decoded, "html.parser")
    source_decoded = str(source_decoded)
    return source_decoded

def save_source(url):
    #add error_codes in the future
    source = ""
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(120)
    try:
        driver.get(url)

    except:
        source = "error"

    if source != "error":

        try:
            time.sleep(10)
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            except:
                pass

            time.sleep(5)
            source = driver.page_source
            source = encode_source(source)

        except Exception as e:
            print(str(e))
            source = "error"

    driver.quit()

    return source

def save_robot_txt(url):

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    try:
        driver.get(url)
        time.sleep(2)
        source = driver.page_source
        try:
            source = encode_source(source)
        except:
            pass

    except:
        source = False

    driver.quit()

    return source

def calculate_loading_time(url):
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(120)
    loading_time = -1

    try:
        driver.get(url)
        time.sleep(5)
        ''' Use Navigation Timing  API to calculate the timings that matter the most '''
        navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
        responseStart = driver.execute_script("return window.performance.timing.responseStart")
        domComplete = driver.execute_script("return window.performance.timing.domComplete")
        loadStart = driver.execute_script("return window.performance.timing.domInteractive")
        EventEnd = driver.execute_script("return window.performance.timing.loadEventEnd")
        ''' Calculate the performance'''
        backendPerformance_calc = responseStart - navigationStart
        frontendPerformance_calc = domComplete - responseStart
        loadingTime = EventEnd - navigationStart
        loading_time = loadingTime / 1000
        driver.quit()
    except Exception as e:
        print(str(e))
        pass

    driver.quit()

    return loading_time



def get_real_url(url):
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(120)
    try:
        driver.get(url)
        time.sleep(4)
        current_url = driver.current_url #read real url (redirected url)
        driver.quit()
        return current_url
    except:
        pass
    driver.quit()
