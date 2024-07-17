from lib.sources import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

from seleniumbase import Driver

from bs4 import BeautifulSoup



import random


def run(query, limit):
    """
    Run the Bing DE scraper.

    Args:
        query (str): The search query.
        limit (int): The maximum number of search results to retrieve.
        scraping: The Scraping object.
        
    Returns:
        list: List of search results.
    """    
    try:
        #Definition of args for scraping the search engine
        language_url = "https://www.bing.com/?cc=de&setLang=de" #URL of search engine
        search_url = "https://www.bing.com/search?q="
        search_box = "sb_form_q.sb_form_ta" #Class name of search box
        search_box = "sb_form_q" #Class name of search box
        captcha = "g-recaptcha" #Source code hint for CAPTCHA
        next_page = "//a[@aria-label='{}']" #CSS to find click on next SERP
        results_number = 0 #initialize results_number
        page = 1 #initialize SERP page
        search_results = [] #initialize search_results list
        limit+=10

        #Definition of custom functions

        #Function to scrape search results
        def get_search_results(driver, page):

            get_search_results = []

            source = driver.page_source

            soup = BeautifulSoup(source, features="lxml")

            for s in soup.find_all("span", class_=["algoSlug_icon"]):
                s.extract()

            for s in soup.find_all("li", class_=["b_algoBigWiki"]):
                s.extract()

            for result in soup.find_all("li", class_=["b_algo", "b_algo_group"]):
                url_list = []
                search_result = []
                result_title = ""
                result_description = ""
                result_url = ""
                try:
                    for title in result.find("a"):
                        result_title+=title.text.strip()
                except:
                    result_title = "N/A"

                try:
                    for description in result.find("p", class_=["b_lineclamp2 b_algoSlug", "b_lineclamp4 b_algoSlug", "b_paractl", "b_lineclamp3 b_algoSlug", "b_lineclamp1 b_algoSlug", "b_dList"]):
                        result_description+=description.text.strip()
                except:
                    try:
                        for description in result.find("ol", class_=["b_dList"]):
                            result_description+=description.text.strip()
                    except:
                        result_description = "N/A"

                try:
                    for url in result.find_all("a"):
                        url = url.attrs['href']
                        if "bing." in url:
                            url = get_real_url(url)
                        url_list.append(url)
                        result_url = url_list[0]
                except:
                    result_url = "N/A"

                if result_url != "N/A" and "http" in result_url:

                    get_search_results.append([result_url])            

            return get_search_results

        #Function to check if search engine shows CAPTCHA code
        def check_captcha(driver):
            source = driver.page_source
            if captcha in source:
                return True
            else:
                return False


        def remove_duplicates(search_results):

            cleaned_search_results = []

            i = 0

            url_list = {}

            for sr in search_results:
                url = sr[0]
                url_list[url] = i
                i = i + 1

            for key, value in url_list.items():                
                cleaned_search_results.append(search_results[value])

            
            return cleaned_search_results

        #initialize Selenium
        #https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/plugins/driver_manager.py For all options
        #https://seleniumbase.io/help_docs/locale_codes/


        driver = Driver(
                browser="chrome",
                wire=True,
                uc=True,
                headless2=True,
                incognito=False,
                do_not_track=True,
                undetectable=True,
                extension_dir=ext_path,
                locale_code="de",
                #mobile=True,
                )

        driver.maximize_window()
        driver.set_page_load_timeout(60)
        driver.implicitly_wait(30)
        driver.get(language_url)
        random_sleep = random.randint(2, 3) #random timer trying to prevent quick automatic blocking
        time.sleep(random_sleep)

        #Start scraping if no CAPTCHA

        if not check_captcha(driver):

            # search = driver.find_element(By.CLASS_NAME, search_box)
            # search.send_keys(query)
            # search.send_keys(Keys.RETURN)

            start = 1
            query = query.lower()
            get_query = query.replace(" ", "+")
            search_results = []

            get_search_url = "https://www.bing.com/search?q={}&qs=n&sp=-1&ghc=1&lq=0&pq={}&sk=&first={}".format(get_query, get_query, start)

            print(get_search_url)

            driver.get(get_search_url)

            random_sleep = random.randint(2, 3) #random timer trying to prevent quick automatic blocking
            time.sleep(random_sleep)             

            search_results = get_search_results(driver, page)

            results_number = len(search_results)

            continue_scraping = True

            start = results_number

            while (results_number <= limit and start <= limit) and continue_scraping:

                if not check_captcha(driver):
                    try:
                        if results_number == start:
                            edit_search_url = get_search_url = "https://www.bing.com/search?q={}&qs=n&sp=-1&ghc=1&lq=0&pq={}&sk=&first={}".format(get_query, get_query, start)
                        else:
                            start = start + 10
                            edit_search_url = get_search_url = "https://www.bing.com/search?q={}&qs=n&sp=-1&ghc=1&lq=0&pq={}&sk=&first={}".format(get_query, get_query, start)
                        print(edit_search_url)
                        driver.get(edit_search_url)
                        random_sleep = random.randint(2, 4) #random timer trying to prevent quick automatic blocking
                        time.sleep(random_sleep)
                        page+=1
                        extract_search_results = get_search_results(driver, page)

                        if len(extract_search_results) > 0:
                            print("go on")
                            search_results+= extract_search_results

                            search_results = remove_duplicates(search_results)

                            results_number = len(search_results)
                           
                            
                        else:
                            continue_scraping = False


                    except Exception as e:
                        print(str(e))
                        continue_scraping = False
                else:
                    continue_scraping = False
                    search_results = -1

            
            driver.quit()                    
            return search_results
                      

        

        else:
            search_results = -1
            driver.quit()
            return search_results
    
    
    except Exception as e:
        print(str(e))
        try:
            driver.quit()
        except:
            pass
        search_results = -1
        return search_results