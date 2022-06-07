#sys libs
import sys
sys.path.insert(0, '..')
from include import *

import urllib.request
from urllib.error import HTTPError

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time



def get_results():
    hashes = Results.getSourcesSpeedNULL()
    return hashes


def pagespeed(hash, url):

    check = Sources.getSpeed(hash)
    speed = -1

    if not check[0][0]:
        print(url)
        print(hash)

        check_source = Results.getResultsSource(hash)

        #print(check_source[0][0])


        if check_source[0][0] != '-1':

            Results.insertSpeed(hash, '-100')

            os.environ['MOZ_HEADLESS'] = '0'
            options = Options()
            #options.add_argument('--ignore-certificate-errors-spki-list')
            #options.add_argument('--ignore-ssl-errors')
            #options.add_argument('--ignore-certificate-errors')
            #options.add_argument('--allow-insecure-localhost')

            options.log.level = 'error'

            profile = webdriver.FirefoxProfile()



            profile.add_extension(extension='/home/sebastian/alpha/extensions/i_dont_care_about_cookies-3.2.7-an+fx.xpi')

            driver = webdriver.Firefox(firefox_profile=profile, options=options)

            driver.set_page_load_timeout(60)


            try:
                driver.get(url)
                time.sleep(10)
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
                speed = loadingTime / 1000

                print(speed)
                driver.quit()
                Results.insertSpeed(hash, speed)

            except:
                print(speed)
                Results.insertSpeed(hash, speed)
                driver.quit()




results = get_results()

for r in results:
    hash = r[0]
    url = r[1]
    pagespeed(hash, url)
