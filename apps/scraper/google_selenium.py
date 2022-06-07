import sys
sys.path.insert(0, '..')
from include import *


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from lxml import html


import time

import random

import pickle

import os

def generate_scraping_job(query, scraper):
    print(query)
    query_string = query[1]
    query_string = query_string.strip()
    query_id = query[4]
    study_id = query[0]
    search_engine = scraper
    #result_pages = 100
    result_pages = 3
    number_multi = 10
    start = 0
    check_jobs = Scrapers.getScrapingJobs(query_id, study_id, search_engine)

    if not check_jobs:
        Scrapers.insertScrapingJobs(query_id, study_id, query_string, search_engine, start, date.today())
        print('Scraper Job: '+query_string+' SE:'+search_engine+' start:'+str(start)+' created')

    #exit()


def scrape_query(query, scraper):

    today = date.today()
    jobs = Scrapers.getScrapingJobsByQueryProgressSE(query, 0, scraper)


    for job in jobs:

        print(job)
        search_engine = job[3]
        search_query = job[2]
        start = job[4]
        query_id = job[0]
        study_id = job[1]
        job_id = job[7]

        progress = 2

        Scrapers.updateScrapingJobQuerySearchEngine(query_id, search_engine, progress)

        Helpers.saveLog("../../logs/"+str(study_id)+"_"+search_query+search_engine+".log", "Start Scraping", 1)

        os.environ['MOZ_HEADLESS'] = '0'

        options = Options()
        #options.add_argument('--ignore-certificate-errors-spki-list')
        #options.add_argument('--ignore-ssl-errors')
        #options.add_argument('--ignore-certificate-errors')
        #options.add_argument('--allow-insecure-localhost')
        options.log.level = 'error'

        profile = webdriver.FirefoxProfile()

        profile.set_preference("browser.safebrowsing.blockedURIs.enabled", True)
        profile.set_preference("browser.safebrowsing.downloads.enabled", True)
        profile.set_preference("browser.safebrowsing.enabled", True)
        profile.set_preference("browser.safebrowsing.forbiddenURIs.enabled", True)
        profile.set_preference("browser.safebrowsing.malware.enabled", True)
        profile.set_preference("browser.safebrowsing.phishing.enabled", True)
        profile.set_preference("dom.webnotifications.enabled", False);

        profile.add_extension(extension='/home/sebastian/alpha/extensions/i_dont_care_about_cookies-3.2.7-an+fx.xpi')

        driver = webdriver.Firefox(firefox_profile=profile, options=options)

        driver.get('http://www.google.de')



        sleeper = random.randint(3,10)


        time.sleep(sleeper)

        try:
            element = driver.find_element_by_id("L2AGLb")
            element.click()

            cookies_file = "cookies_google.pkl"

            if os.path.exists(cookies_file):
                if os.path.getmtime(cookies_file) < now - 1 *86400:
                    os.remove(cookies_file)
                    pickle.dump(driver.get_cookies(), open(cookies_file, "wb"))

                else:
                    cookies = pickle.load(open(cookies_file, "rb"))

                    for cookie in cookies:
                        driver.add_cookie(cookie)
            else:
                pickle.dump(driver.get_cookies(), open(cookies_file, "wb"))

                for cookie in cookies:
                    driver.add_cookie(cookie)

        except:
            pass

        sleeper = random.randint(3,10)

        time.sleep(sleeper)

        search = driver.find_element_by_name('q')
        search.send_keys(search_query)
        search.send_keys(Keys.RETURN)

        sleeper = random.randint(6,10)

        time.sleep(sleeper)

        check_source = driver.page_source

        #print(check_source)

        if str(check_source).find(str("g-recaptcha")) > 0:
            print("CAPTCHA")
            Helpers.saveLog("../../logs/"+str(study_id)+"_"+search_query+".log", 'Error Scraping Job', 1)
            Scrapers.updateScrapingJobQuerySearchEngine(query_id, search_engine, -1)
            Results.deleteResultsNoScrapers(query_id, search_engine)
            driver.quit()
            exit()

        xpath_res = "//div[@class='tF2Cxc']/div[@class='yuRUbf']/a/@href"

        pages = []

        results = []

        source = driver.page_source

        tree = html.fromstring(source)
        urls = tree.xpath(xpath_res)

        for url in urls:
            results.append(url)

        number_pages = 4

        x = range(2, number_pages)

        for n in x:
            r = str(n)
            page = 'Page '+r
            pages.append(page)


        for p in pages:

            print(p)

            xpath = "//a[@aria-label='{}']".format(p)

            try:

                paging = driver.find_element_by_xpath(xpath)

                paging.click()

                sleeper = random.randint(6,10)

                time.sleep(sleeper)

                source = driver.page_source

                check_source = driver.page_source

                #print(check_source)

                if str(check_source).find(str("g-recaptcha")) > 0:
                    print("CAPTCHA")
                    Helpers.saveLog("../../logs/"+str(study_id)+"_"+search_query+".log", 'Error Scraping Job', 1)
                    Scrapers.updateScrapingJobQuerySearchEngine(query_id, search_engine, -1)
                    Results.deleteResultsNoScrapers(query_id, search_engine)
                    driver.quit()
                    exit()

                tree = html.fromstring(source)
                urls = tree.xpath(xpath_res)

                for url in urls:
                    results.append(url)

            except:
                pass

        print(results)

        driver.quit()

        if results:
            Scrapers.updateScrapingJobQuerySearchEngine(query_id, search_engine, 1)
            results_position = 0
            for result in results:
                url = result
                check_url = Results.getURL(query_id, study_id, url, search_engine)

                if (not check_url):
                    results_position = results_position + 1
                    url_meta = Results.getResultMeta(url, str(study_id), search_engine, str(query_id))
                    hash = url_meta[0]
                    ip = url_meta[1]
                    main = url_meta[2]
                    main_hash = Helpers.computeMD5hash(main+str(study_id)+search_engine+str(query_id))
                    contact_url = "0"
                    Helpers.saveLog("../../logs/"+str(study_id)+"_"+search_query+".log", url, 1)
                    contact_hash = "0"
                    contact_url = "0"

                    Results.insertResult(query_id, study_id, job_id, 0, ip, hash, main_hash, contact_hash, search_engine, url, main, contact_url, today, datetime.now(), 1, results_position)

                    check_sources = Results.getSource(hash)
                    if not check_sources:
                        Helpers.saveLog("../../logs/"+str(study_id)+"_"+search_query+".log", 'Insert Result', 1)
                        Results.insertSource(hash, None, None, None, today, 0)




try:
    studies = Studies.getStudiesScraper()

    for s in studies:
        if  s[-1] == "Google_Selenium":
            scraper = "Google_Selenium"

            studies_id = s[-3]

            print(studies_id)

            queries = Queries.getQueriesStudy(studies_id)

            scraping_jobs = Scrapers.getScrapingJobsByStudyQueries(studies_id)

            c_q = len(queries)
            c_s = scraping_jobs[0][0]

            if c_s < c_q:

                for q in queries:
                    query_id = q[-2]

                    job = 0
                    check_jobs = Scrapers.getScrapingJobsBySE(query_id, scraper)
                    count_jobs = check_jobs[0][0]
                    if count_jobs == 0:
                        job = 1

                    if job == 1:
                        generate_scraping_job(q, scraper)

            if not(Scrapers.getScrapingJobsByProgressSE(-1, scraper)):

                open_queries = Queries.getOpenQueriesStudybySE(studies_id, scraper)

                if open_queries:
                    random.shuffle(open_queries)
                    o = open_queries[0]



                    if o:
                        check_progress = Scrapers.getScrapingJobsByQueryProgressSE(o, 2, scraper)
                        if not check_progress:
                            print(o)
                            scrape_query(o, scraper)
                            exit()

except Exception as e:
    print("Error")
    print(e)
