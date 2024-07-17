import os
import inspect

from pathlib import Path

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

parentdir = os.path.dirname(currentdir)


ext_path = parentdir+"/i_care_about_cookies_unpacked"

from seleniumbase import Driver

import time


import time

import os
current_path = os.path.abspath(os.getcwd())

import base64

from bs4 import BeautifulSoup


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
    driver = Driver(
            browser="chrome",
            wire=True,
            uc=True,
            headless2=True,
            incognito=False,
            agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            do_not_track=True,
            undetectable=True,
            extension_dir=ext_path,
            locale_code="de",
            no_sandbox=True,
            )
    
    driver.implicitly_wait(30)
    driver.set_page_load_timeout(120)

    #add error_codes in the future
    source = ""
    try:
        driver.get(url)
        time.sleep(10)

    except:
        source = "error"

    if source != "error":

        try:
            
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

    driver = Driver(
            browser="chrome",
            wire=True,
            uc=True,
            headless2=True,
            incognito=False,
            agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            do_not_track=True,
            undetectable=True,
            extension_dir=ext_path,
            locale_code="de",
            no_sandbox=True,
            )    

    driver.set_page_load_timeout(30)
    driver.implicitly_wait(30)
    
    try:
        driver.get(url)
        time.sleep(5)
        source = driver.page_source
        try:
            source = encode_source(source)
        except:
            pass

    except:
        source = False

    driver.quit()

    return source

def get_real_url(url):

    driver = Driver(
            browser="chrome", 
            wire=True,
            uc=True,
            headless2=True,
            incognito=False,
            agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            do_not_track=True,
            undetectable=True,
            extension_dir=ext_path,
            locale_code="de",
            no_sandbox=True,
            )    

    driver.set_page_load_timeout(30)
    driver.implicitly_wait(30)
    try:
        driver.get(url)
        time.sleep(4)
        current_url = driver.current_url #read real url (redirected url)
        driver.quit()
        return current_url
    except:
        pass
    driver.quit()


