#sys libs
import os, sys
import os.path
import json

#scraping libs
from urllib.parse import urlsplit
from os.path import isfile, join
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time

from lxml import html
from bs4 import BeautifulSoup, Comment
import lxml.html
import os

from urllib.parse import urlsplit
from urllib.parse import urlparse
import urllib.parse
import socket

#tool libs
sys.path.insert(0, '..')
from db.connect import DB

sys.path.insert(0, '..')
from db.results import Results as DB_Results

from libs.helpers import Helpers

# class for results functions; mainly to read and write database content but also to save the source code of URLs
class Results:

    def __init__(self, cursor):
        self.cursor = cursor

    def saveResult(url):

        os.environ['MOZ_HEADLESS'] = '0'
        options = Options()
        #options.add_argument('--ignore-certificate-errors-spki-list')
        #options.add_argument('--ignore-ssl-errors')
        #options.add_argument('--ignore-certificate-errors')
        #options.add_argument('--allow-insecure-localhost')
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

        profile.add_extension(extension='/home/sebastian/alpha/extensions/i_dont_care_about_cookies-3.2.7-an+fx.xpi')

        driver = webdriver.Firefox(firefox_profile=profile, options=options)

        driver.set_page_load_timeout(60)


        try:
            driver.get(url)
            time.sleep(10)
            source = driver.page_source


        except:
            source = "error"

        driver.quit()

        source = Helpers.changeCoding(source)

        return source

    def getResultMeta(url, study_id, search_engine, query_id):
        meta = []
        study_id = str(study_id)
        query_id = str(query_id)
        compute_hash = url+study_id+search_engine+query_id
        hash = Helpers.computeMD5hash(compute_hash)
        try:
                parsed_uri = urlparse(url)
                #o = urllib.parse.urlsplit(url)
                #hostname = o.hostname
                hostname = '{uri.netloc}'.format(uri=parsed_uri)
                ip = socket.gethostbyname(hostname)
        except:
            ip = "-1"
        main = '{0.scheme}://{0.netloc}/'.format(urlsplit(url))
        meta = [hash, ip, main]
        return meta

    def getContent(source, main):
        content = []
        comments = ""
        urls = ""



        if (source !="error"):
            #extract all comments in source code
            soup = BeautifulSoup(source, 'lxml')
            comments_bs4 = soup.findAll(text=lambda text:isinstance(text, Comment))


            for c in comments_bs4:
                c = Helpers.html_escape(c)
                if c and c != " ":
                    comments = comments+'[comment_source]'+c


            soup_urls = []
            tags = soup.find_all('a')

            for tag in tags:
                link_text = str(tag.string).strip()
                href = str(tag.get('href')).strip()
                if "http" not in href:
                    href = href.lstrip('/')
                    href = main+href

                link = "[url]"+link_text+"   "+href
                if not Helpers.matchText(link, '*mailto:*'):
                    link = Helpers.html_escape(link)
                    if link and link != " ":
                        urls = urls+link

            content = [Helpers.html_escape(str(source)), urls, comments]
            return content


    def getContactUrl(urls, main):

        with open('../config/evaluation.ini', 'r') as f:
            array = json.load(f)

        config_file = array["crawler"]["contact"]["config"]

        with open(config_file, 'r') as f:
            array = json.load(f)

        keywords = array["keywords"]

        contact_urls = []

        urls = urls.split('[url]')

        for keyword in keywords:

            for url in urls:

                if(url):
                    href = url.split("  ")
                    if len(href) > 1:
                        link = href[1]
                        anchor = href[0]
                        pattern = "*"+keyword+"*"
                        if Helpers.matchText(link, pattern) or Helpers.matchText(anchor, pattern):
                            contact_urls.append([link, keyword])

        contact_urls = Helpers.remove_duplicates_from_list(contact_urls)

        if(contact_urls):
            check = contact_urls[0][0]

            if Helpers.matchText(check, "*http*//*"):
                contact_url = check
            else:

                if Helpers.matchText(check, "*..*"):
                    check = check.replace('..', '')
                    check = "".join(check.split())
                contact_url = main+check

        else:
            contact_url = "-1"

        return contact_url

    def getRecentSource(hash):
        db = DB()
        rows = DB_Results.getRecentSource(db.cursor, hash)
        db.DBDisconnect()
        return rows

    def getResultsSource(hash):
        db = DB()
        rows = DB_Results.getResultsSource(db.cursor, hash)
        db.DBDisconnect()
        return rows

    def insertSource(hash, source, urls, comments, today, progress):
        db = DB()
        DB_Results.insertSource(db.cursor, hash, source, urls, comments, today, progress)
        db.DBDisconnect()

    def updateSources(hash, source, urls, comments, today, progress):
        db = DB()
        DB_Results.updateSources(db.cursor, hash, source, urls, comments, today, progress)
        db.DBDisconnect()

    def insertSpeed(hash, speed):
        db = DB()
        DB_Results.insertSpeed(db.cursor, hash, speed)
        db.DBDisconnect()

    def getSpeed(hash):
        db = DB()
        rows = DB_Results.getSpeed(db.cursor, hash)
        db.DBDisconnect()
        return rows

    def getResultsSourcesNULL():
        db = DB()
        rows = DB_Results.getResultsSourcesNULL(db.cursor)
        db.DBDisconnect()
        return rows

    def insertResult(query_id, study_id, job_id, upload, ip, hash, main_hash, contact_hash, search_engine, url, main, contact, today, timestamp, progress, results_position):
        db = DB()
        DB_Results.insertResult(db.cursor, query_id, study_id, job_id, upload, ip, hash, main_hash, contact_hash, search_engine, url, main, contact, today, timestamp, progress, results_position)
        db.DBDisconnect()

    def getAllResultsIdsByStudy(results_studies_id):
        db = DB()
        rows = DB_Results.getAllResultsIdsByStudy(db.cursor, results_studies_id)
        db.DBDisconnect()
        return rows

    def getResultsIdsByStudyContact(results_studies_id, results_contact):
        db = DB()
        rows = DB_Results.getResultsIdsByStudyContact(db.cursor, results_studies_id, results_contact)
        db.DBDisconnect()
        return rows

    def getResultById(results_id):
        db = DB()
        rows = DB_Results.getResultById(db.cursor, results_id)
        db.DBDisconnect()
        return rows

    def getResultByHash(hash):
        db = DB()
        rows = DB_Results.getResultByHash(db.cursor, hash)
        db.DBDisconnect()
        return rows

    def insertContactResult(contact_url, contact_hash, results_id):
        db = DB()
        DB_Results.insertContactResult(db.cursor, contact_url, contact_hash, results_id)
        db.DBDisconnect()


    def updateContactProgress(results_contact, results_id):
        db = DB()
        DB_Results.updateContactProgress(db.cursor, results_contact, results_id)
        db.DBDisconnect()


    def getRecentResultByHash(hash):
        db = DB()
        rows = DB_Results.getRecentResultByHash(db.cursor, hash)
        db.DBDisconnect()
        return rows

    def getResults():
        db = DB()
        rows = DB_Results.getResults(db.cursor)
        db.DBDisconnect()
        return rows


    def getSourcesSpeedNULL():
        db = DB()
        rows = DB_Results.getSourcesSpeedNULL(db.cursor)
        db.DBDisconnect()
        return rows

    def getLastPosition(query_id, study_id, results_se, today):
        db = DB()
        rows = DB_Results.getLastPosition(db.cursor, query_id, study_id, results_se, today)
        db.DBDisconnect()
        return rows

    def countResultsbyStudy(studies_id):
        db = DB()
        rows = DB_Results.countResultsbyStudy(db.cursor, studies_id)
        db.DBDisconnect()
        return rows

    def countResultsbyStudySE(studies_id, se):
        db = DB()
        rows = DB_Results.countResultsbyStudySE(db.cursor, studies_id, se)
        db.DBDisconnect()
        return rows

    def countResultsQuery(results_queries_id):
        db = DB()
        rows = DB_Results.countResultsQuery(db.cursor, results_queries_id)
        db.DBDisconnect()
        return rows

    def countClassifiedResultsbyQuery(results_queries_id):
        db = DB()
        rows = DB_Results.countClassifiedResultsbyQuery(db.cursor, results_queries_id)
        db.DBDisconnect()
        return rows

    def countClassifiedResultsbyStudy(studies_id):
        db = DB()
        rows = DB_Results.countClassifiedResultsbyStudy(db.cursor, studies_id)
        db.DBDisconnect()
        return rows

    def countClassifiedResultsbyStudySE(studies_id, se):
        db = DB()
        rows = DB_Results.countClassifiedResultsbyStudySE(db.cursor, studies_id, se)
        db.DBDisconnect()
        return rows

    def countFailedResultsbyStudy(studies_id):
        db = DB()
        rows = DB_Results.countFailedResultsbyStudy(db.cursor, studies_id)
        db.DBDisconnect()
        return rows

    def getPosition(query_id, study_id, search_engine, results_position):
        db = DB()
        rows = DB_Results.getPosition(db.cursor, query_id, study_id, search_engine, results_position)
        db.DBDisconnect()
        return rows

    def getResultHashesOnMain(main_hash):
        db = DB()
        rows = DB_Results.getResultHashesOnMain(db.cursor, main_hash)
        db.DBDisconnect()
        return rows

    def getSource(hash):
        db = DB()
        rows = DB_Results.getSource(db.cursor, hash)
        db.DBDisconnect()
        return rows

    def getURL(query_id, study_id, results_url, results_se):
        db = DB()
        rows = DB_Results.getURL(db.cursor, query_id, study_id, results_url, results_se)
        db.DBDisconnect()
        return rows

    def getSERP(query_id):
        db = DB()
        DB_Results.getSERP(db.cursor, query_id)
        db.DBDisconnect()

    def insertSERP(query_id, serp, serp_scraper, today):
        db = DB()
        DB_Results.insertSERP(db.cursor, query_id, serp, serp_scraper, today)
        db.DBDisconnect()


    def getLastPosition(query_id, study_id, search_engine, results_position):
        db = DB()
        rows = DB_Results.getLastPosition(db.cursor, query_id, study_id, search_engine, results_position)
        db.DBDisconnect()
        return rows

    def deleteResults(queries_id, results_se):
        db = DB()
        DB_Results.deleteResults(db.cursor, queries_id, results_se)
        db.DBDisconnect()

    def deleteResultsNoScrapers(queries_id, results_se):
        db = DB()
        DB_Results.deleteResultsNoScrapers(db.cursor, queries_id, results_se)
        db.DBDisconnect()
