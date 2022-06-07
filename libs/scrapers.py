#sys libs
import os, sys
import os.path
import json
from datetime import date
import random
import time
import csv

#scraping libs
from os.path import isfile, join
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from lxml import html

#from fake_useragent import UserAgent

#tool libs
sys.path.insert(0, '..')
from db.connect import DB

sys.path.insert(0, '..')
from db.scrapers import Scrapers as DB_Scrapers

from libs.helpers import Helpers

class Scrapers:
    def __init__(self, search_engine, results_range, search_url, start_parameter, start_add, number_parameter, number_multi, number_div, xpath, filter, serp_filter, language):
        self.__search_engine = search_engine
        self.__results_range = results_range
        self.__search_url = search_url
        self.__start_parameter = start_parameter
        self.__start_add = start_add
        self.__number_parameter = number_parameter
        self.__number_multi = number_multi
        self.__number_div = number_div
        self.__xpath = xpath
        self.__filter = filter
        self.__serp_filter = serp_filter
        self.__language = language

    def __getResultsRange(self):
        return self.__results_range

    results_range = property(__getResultsRange)

    def __getSearchEngine(self):
        return self.__search_engine

    search_engine = property(__getSearchEngine)

    def __getSearchURL(self):
        return self.__search_url

    search_url = property(__getSearchURL)


    def __getXpath(self):
        return self.__xpath

    xpath = property(__getXpath)

    def __getStartParameter(self):
        return self.__start_parameter

    start = property(__getStartParameter)

    def __getStartAdd(self):
        return self.__start_add

    start_add = property(__getStartAdd)

    def __getNumberParameter(self):
        return self.__number_parameter

    number_parameter = property(__getNumberParameter)

    def __getNumberMulti(self):
        return self.__number_multi

    number_multi = property(__getNumberMulti)

    def __getNumberDiv(self):
        return self.__number_div

    number_div = property(__getNumberDiv)

    def __getFilterParameter(self):
        return self.__filter

    filter = property(__getFilterParameter)

    def __getSERPFilterParameter(self):
        return self.__serp_filter

    serp_filter = property(__getSERPFilterParameter)

    def __getLanguage(self):
        return self.__language

    language = property(__getLanguage)

    def genProxies():

        proxy_url = "https://hidemy.name/de/proxy-list/?type=s#list"

        os.environ['MOZ_HEADLESS'] = '0'

        profile = webdriver.FirefoxProfile()

        profile.set_preference("browser.safebrowsing.blockedURIs.enabled", True)
        profile.set_preference("browser.safebrowsing.downloads.enabled", True)
        profile.set_preference("browser.safebrowsing.enabled", True)
        profile.set_preference("browser.safebrowsing.forbiddenURIs.enabled", True)
        profile.set_preference("browser.safebrowsing.malware.enabled", True)
        profile.set_preference("browser.safebrowsing.phishing.enabled", True)
        profile.set_preference("dom.webnotifications.enabled", False);


        driver = webdriver.Firefox(firefox_profile=profile)

        driver.set_page_load_timeout(60)

        driver.get(proxy_url)

        source = driver.page_source

        driver.quit()

        tree = html.fromstring(source)

        ips = "//div[@class='table_block']//tr//td[1]/text()"
        ports = "//div[@class='table_block']//tr//td[2]/text()"


        ip = tree.xpath(ips)

        port = tree.xpath(ports)

        y = 0

        proxies = []

        for i in ip:
            proxy = i+":"+port[y]
            y = y + 1
            proxies.append(proxy)


        proxies = proxies[1:]

        file = "proxies.csv"

        with open(file,'w+') as f:
            f.close()


        with open(file,'a+') as f:
            for p in proxies:
                f.write(p+'\n')
        f.close()

        return proxies


    def scrapeQuery(query, search_xpath, start, filter):

        def extractSearchResults(source, xpath):
            tree = html.fromstring(source)
            urls = tree.xpath(xpath)
            return urls


        def useProxy(query, search_xpath, start, filter):




                proxy_file = "proxies.csv"

                proxies = []

                with open(proxy_file, newline='') as inputfile:
                    for row in csv.reader(inputfile):
                        proxies.append(row[0])


                for p in proxies:

                    print(p)

                    try:

                        today = date.today()
                        string_today = str(today)
                        results = []


                        firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
                        firefox_capabilities['marionette'] = True

                        PROXY = p

                        firefox_capabilities['proxy'] = {
                            "proxyType": "MANUAL",
                            "httpProxy": PROXY,
                            "ftpProxy": PROXY,
                            "sslProxy": PROXY
                        }

                        os.environ['MOZ_HEADLESS'] = '0'

                        options = Options()

                        '''
                        ua = UserAgent()
                        userAgent = ua.random
                        print(userAgent)
                        options.add_argument(f'user-agent={userAgent}')
                        '''

                        options.add_argument("user-data-dir=selenium")
                        options.log.level = 'error'

                        profile = webdriver.FirefoxProfile()

                        profile.set_preference("browser.safebrowsing.blockedURIs.enabled", True)
                        profile.set_preference("browser.safebrowsing.downloads.enabled", True)
                        profile.set_preference("browser.safebrowsing.enabled", True)
                        profile.set_preference("browser.safebrowsing.forbiddenURIs.enabled", True)
                        profile.set_preference("browser.safebrowsing.malware.enabled", True)
                        profile.set_preference("browser.safebrowsing.phishing.enabled", True)
                        profile.set_preference("dom.webnotifications.enabled", False);

                        #profile.add_extension(extension='/home/sebastian/alpha/extensions/i_dont_care_about_cookies-3.2.7-an+fx.xpi')

                        driver = webdriver.Firefox(firefox_profile=profile, options=options, capabilities=firefox_capabilities)

                        driver.set_page_load_timeout(60)

                        sleeper = random.randint(3,10)

                        time.sleep(sleeper)

                        print(query)

                        driver.get(query)

                        source = driver.page_source

                        source = Helpers.changeCoding(source)

                        print(source)

                        xpath = search_xpath

                        urls = extractSearchResults(source, xpath)

                        print(urls)

                        driver.quit()

                        if str(source).find(str("g-recaptcha-response")) > 0:
                            print("CAPTCHA")
                            pass

                        else:

                            xpath = search_xpath

                            urls = extractSearchResults(source, xpath)

                            i = start

                            if urls:
                                for url in urls:
                                    i = i + 1
                                    results.append(url)

                            search_results = list(dict.fromkeys(results))

                            res = []

                            if search_results:
                                res = [search_results, source]
                                return res
                            else:
                                if str(source).find(str(filter)) > 0:
                                    res = ["filtered", source]
                                    return res
                                else:
                                    print(source)
                                    return False


                    except:
                        driver.quit()
                        pass


        today = date.today()
        string_today = str(today)
        results = []

        check_filter = filter.split(';')

        os.environ['MOZ_HEADLESS'] = '0'


        options = Options()

        '''
        ua = UserAgent()
        userAgent = ua.random
        print(userAgent)
        options.add_argument(f'user-agent={userAgent}')
        '''

        options.add_argument("user-data-dir=selenium")
        options.log.level = 'error'

        profile = webdriver.FirefoxProfile()

        profile.set_preference("browser.safebrowsing.blockedURIs.enabled", True)
        profile.set_preference("browser.safebrowsing.downloads.enabled", True)
        profile.set_preference("browser.safebrowsing.enabled", True)
        profile.set_preference("browser.safebrowsing.forbiddenURIs.enabled", True)
        profile.set_preference("browser.safebrowsing.malware.enabled", True)
        profile.set_preference("browser.safebrowsing.phishing.enabled", True)
        profile.set_preference("dom.webnotifications.enabled", False);

        #profile.add_extension(extension='/home/sebastian/alpha/extensions/i_dont_care_about_cookies-3.2.7-an+fx.xpi')

        driver = webdriver.Firefox(firefox_profile=profile, options=options)

        driver.set_page_load_timeout(60)

        sleeper = random.randint(3,10)

        time.sleep(sleeper)

        driver.get(query)

        source = driver.page_source

        source = Helpers.changeCoding(source)

        xpath = search_xpath

        urls = extractSearchResults(source, xpath)

        driver.quit()

        i = start

        if urls:
            for url in urls:
                i = i + 1
                results.append(url)

        search_results = list(dict.fromkeys(results))

        res = []


        if search_results:
            res = [search_results, source]
            return res
        else:
            if str(source).find(str("g-recaptcha-response")) > 0:
                print("CAPTCHA")
                print(source)
                return False
            else:
                res = ["filtered", source]
                return res
                '''
                for c in check_filter:
                    if str(source).find(str(c)) > 0:
                        res = ["filtered", source]
                        return res
                '''
                #useProxy(query, search_xpath, start, filter)









    def generateScrapers():
    #noch dynamischer generieren einfach nach anzahl der scraper, nicht mit google_config und bing_config
        with open('../../config/scraper.ini', 'r') as f:
            array = json.load(f)

        scrapers_json = array['scraper']

        scrapers = []

        for scraper in scrapers_json:
            config = scrapers_json[scraper]
            search_engine = config['search_engine']
            results_range = config['results_range']
            search_url = config['search_url']
            start_parameter = config['start_parameter']
            start_add = config['start_add']
            number_parameter = config['number_parameter']
            number_multi = config['number_multi']
            number_div = config['number_div']
            xpath = config['xpath']
            filter = config['filter']
            serp_filter = config['serp_filter']
            language = config['language']
            scrapers.append(Scrapers(search_engine, results_range, search_url, start_parameter, start_add, number_parameter, number_multi, number_div, xpath, filter, serp_filter, language))

        return scrapers

    def getScrapingJobsByProgress(progress):
        db = DB()
        rows = DB_Scrapers.getScrapingJobsByProgress(db.cursor, progress)
        db.DBDisconnect()
        return rows

    def getScrapingJobsByProgressSE(progress, se):
        db = DB()
        rows = DB_Scrapers.getScrapingJobsByProgressSE(db.cursor, progress, se)
        db.DBDisconnect()
        return rows

    def insertScrapingJobs(query_id, study_id, query_string, search_engine, start, today):
        db = DB()
        rows = DB_Scrapers.insertScrapingJobs(db.cursor, query_id, study_id, query_string, search_engine, start, today)
        db.DBDisconnect()

    def getScrapingJobsByQueryProgress(query_id, progress):
        db = DB()
        rows = DB_Scrapers.getScrapingJobsByQueryProgress(db.cursor, query_id, progress)
        db.DBDisconnect()
        return rows

    def getScrapingJobsByQueryProgressSE(query_id, progress, se):
        db = DB()
        rows = DB_Scrapers.getScrapingJobsByQueryProgressSE(db.cursor, query_id, progress, se)
        db.DBDisconnect()
        return rows

    def getScrapingJobsByQuery(query):
        db = DB()
        rows = DB_Scrapers.getScrapingJobsByQuery(db.cursor, query)
        db.DBDisconnect()
        return rows

    def getScrapingJobsBySE(query_id, search_engine):
        db = DB()
        rows = DB_Scrapers.getScrapingJobsBySE(db.cursor, query_id, search_engine)
        db.DBDisconnect()
        return rows


    def updateScrapingJobQuery(query_id, progress):
        db = DB()
        DB_Scrapers.updateScrapingJobQuery(db.cursor, query_id, progress)
        db.DBDisconnect()

    def updateScrapingJobQuerySeJobId(query_id, progress, se, job_id):
        db = DB()
        DB_Scrapers.updateScrapingJobQuerySeJobId(db.cursor, query_id, progress, se, job_id)
        db.DBDisconnect()

    def updateScrapingJobQuerySearchEngine(query_id, search_engine, progress):
        db = DB()
        DB_Scrapers.updateScrapingJobQuerySearchEngine(db.cursor, query_id, search_engine, progress)
        db.DBDisconnect()

    def updateScrapingJob(job_id, progress):
        db = DB()
        DB_Scrapers.updateScrapingJob(db.cursor, job_id, progress)
        db.DBDisconnect()

    def resetScrapingJobs():
        db = DB()
        DB_Scrapers.resetScrapingJobs(db.cursor)
        db.DBDisconnect()

    def getScrapingJobs(query_id, study_id, search_engine):
        db = DB()
        DB_Scrapers.getScrapingJobs(db.cursor, query_id, study_id, search_engine)
        db.DBDisconnect()

    def getScrapingJobsByStudyQueries(study):
        db = DB()
        rows = DB_Scrapers.getScrapingJobsByStudyQueries(db.cursor, study)
        db.DBDisconnect()
        return rows
