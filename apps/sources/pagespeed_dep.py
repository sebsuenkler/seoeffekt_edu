#sys libs
import sys
sys.path.insert(0, '..')
from include import *

import urllib.request
from urllib.error import HTTPError


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

            try:
                urllib.request.urlretrieve(url)

            except:

                Results.insertSpeed(hash, speed)

                print(speed)

            else:
                try:
                    options = Options()
                    options.add_argument('--ignore-certificate-errors-spki-list')
                    options.add_argument('--ignore-ssl-errors')
                    options.add_argument('--ignore-certificate-errors')
                    options.add_argument('--allow-insecure-localhost')
                    options.add_argument('--disable-extensions')
                    options.add_argument('--no-sandbox')
                    options.add_argument('-headless')
                    options.log.level = 'error'
                    options.headless = True

                    driver = webdriver.Firefox(options=options)
                    driver.set_page_load_timeout(20)
                    driver.set_script_timeout(20)
                    driver.get(url)


                    speed = driver.execute_script(
                                """
                                var loadTime = ((window.performance.timing.domComplete- window.performance.timing.navigationStart)/1000);
                                return loadTime;
                                """
                                    )
                    driver.quit()



                    Results.insertSpeed(hash, speed)

                    print(speed)

                except Exception as e:
                    driver.quit()
                    Results.insertSpeed(hash, speed)

                    #exit()

        else:
            Results.insertSpeed(hash, speed)
            print(speed)

results = get_results()

print(results)

for r in results:
    hash = r[0]
    url = r[1]
    pagespeed(hash, url)
