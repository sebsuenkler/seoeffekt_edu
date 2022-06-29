import sqlite3 as sl

import datetime

from lib.sources import get_real_url

def write_to_log(timestamp, content):
    f = open("main.log", "a+")
    f.write(timestamp+": "+content+"\n")
    f.close()


def connect_to_db():
    connection = sl.connect('seo_effect.db', timeout=10, isolation_level=None)
    connection.execute('pragma journal_mode=wal')
    return connection

def close_connection_to_db(connection):
    connection.close()

scraper_id = 0
reset_id = 0

connection = connect_to_db()
cursor = connection.cursor()
data = cursor.execute("SELECT id FROM SCRAPER WHERE progress =? ORDER BY RANDOM() LIMIT 1", (-1,))
connection.commit()
for row in data:
    reset_id = row[0]

close_connection_to_db(connection)

if reset_id == 0:

    connection = connect_to_db()
    cursor = connection.cursor()
    data = cursor.execute("SELECT * FROM SCRAPER WHERE progress =? ORDER BY RANDOM() LIMIT 1", (0,))
    connection.commit()

    for row in data:
        scraper_id = row[0]
        study_id = row[1]
        query_id = row[2]
        query = row[3]
        search_engine = row[4]
    close_connection_to_db(connection)

    if scraper_id != 0:

        timestamp = datetime.datetime.now()
        timestamp = timestamp.strftime("%d-%m-%Y, %H:%M:%S")

        write_to_log(timestamp, "Scrape "+str(search_engine)+" Job_Id:"+str(scraper_id)+" Query:"+str(query)+" started")

        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("UPDATE SCRAPER SET progress =? WHERE id =?", (2,scraper_id,))
        connection.commit()
        close_connection_to_db(connection)


        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.firefox.options import Options
        import time

        from lxml import html
        from bs4 import BeautifulSoup

        import json

        with open('scraper.json') as json_file:
            search_engines_json = json.load(json_file)

        search_box = search_engines_json[search_engine]['search-box']
        max_number_pages = search_engines_json[search_engine]['max_number_pages']
        xpath_next_page = search_engines_json[search_engine]['xpath_next_page']
        search_url = search_engines_json[search_engine]['search_url']
        xpath_results = search_engines_json[search_engine]['xpath_results']
        max_results_filter = search_engines_json[search_engine]['max_results_filter']
        captcha = search_engines_json[search_engine]['captcha']
        redirect = search_engines_json[search_engine]['redirect']

        search_results = []
        pages = []

        import os
        current_path = os.path.abspath(os.getcwd())

        if os.name == "nt":
            extension_path = current_path+"\i_dont_care_about_cookies-3.4.0.xpi"

        else:
            extension_path = current_path+"/i_dont_care_about_cookies-3.4.0.xpi"


        def get_search_results(driver):
            source = driver.page_source
            tree = html.fromstring(source)
            found_urls = tree.xpath(xpath_results)
            urls = []
            for f_url in found_urls:
                if redirect == "true":
                    url = get_real_url(f_url)
                else:
                    url = f_url
                urls.append(url)
            return urls

        def check_captcha(driver):
            source = driver.page_source
            if captcha in source:
                return True
            else:
                return False

        def check_max_results(driver):
            source = driver.page_source
            if max_results_filter in source and max_results_filter != "check_last_result":
                return True
            else:
                return False


        options = Options()
        options.headless = True

        driver = webdriver.Firefox(options=options)
        driver.install_addon(extension_path, temporary=False)
        driver.get(search_url)
        time.sleep(2)
        search = driver.find_element(By.NAME, search_box)
        search.send_keys(query)
        search.send_keys(Keys.RETURN)
        time.sleep(2)

        if not check_captcha(driver):
            blocked = False

            urls = get_search_results(driver)



            search_results.append(urls)

            init_page = 2

            x = range(init_page, init_page+max_number_pages)

            for n in x:
                r = str(n)
                page = 'Page '+r
                pages.append(page)

            for p in pages:

                if not check_max_results(driver):

                    time.sleep(2)

                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                    next_page = driver.find_element(By.XPATH, xpath_next_page.format(p))

                    next_page.click()

                    time.sleep(2)

                    urls = get_search_results(driver)



                    search_results.append(urls)

                else:
                    pass
        else:
            blocked = True

        driver.quit()

        if blocked:
            connection = connect_to_db()
            cursor = connection.cursor()
            cursor.execute("UPDATE SCRAPER SET progress =? WHERE id =?", (-1,scraper_id,))
            connection.commit()
            close_connection_to_db(connection)

            timestamp = datetime.datetime.now()
            timestamp = timestamp.strftime("%d-%m-%Y, %H:%M:%S")

            write_to_log(timestamp, "Scrape "+str(search_engine)+" Job_Id:"+str(scraper_id)+" Query:"+str(query)+" failed [CAPTCHA]")

        else:
            connection = connect_to_db()
            cursor = connection.cursor()
            cursor.execute("UPDATE SCRAPER SET progress =? WHERE id =?", (1,scraper_id,))
            connection.commit()
            close_connection_to_db(connection)

            timestamp = datetime.datetime.now()
            timestamp = timestamp.strftime("%d-%m-%Y, %H:%M:%S")

            write_to_log(timestamp, "Scrape "+str(search_engine)+" Job_Id:"+str(scraper_id)+" Query:"+str(query)+" success")


            import datetime
            from datetime import date
            today = date.today()
            timestamp = datetime.datetime.now()

            from urllib.parse import urlsplit
            from urllib.parse import urlparse
            import socket

            def get_meta(url):
                meta = []
                try:
                    parsed_uri = urlparse(url)
                    hostname = '{uri.netloc}'.format(uri=parsed_uri)
                    ip = socket.gethostbyname(hostname)
                except:
                    ip = "-1"

                main = '{0.scheme}://{0.netloc}/'.format(urlsplit(url))
                meta = [ip, main]
                return meta

            position = 0

            for urls in search_results:

                for url in urls:

                    meta = get_meta(url)

                    ip = meta[0]
                    main_url = meta[1]

                    position+=1

                    connection = connect_to_db()
                    cursor = connection.cursor()
                    sql = 'INSERT INTO SEARCH_RESULT(study_id, query_id, scraper_id, ip, search_engine, position, url, main_url, timestamp, date) values(?,?,?,?,?,?,?,?,?,?)'
                    data = (study_id, query_id, scraper_id, ip, search_engine, position, url, main_url, timestamp, today)
                    cursor.execute(sql, data)
                    connection.commit()
                    result_id = cursor.lastrowid
                    close_connection_to_db(connection)

                    connection = connect_to_db()
                    cursor = connection.cursor()
                    sql = 'INSERT INTO SOURCE(result_id, scraper_id, progress, date) values(?,?,?,?)'
                    data = (result_id, scraper_id, 0, today)
                    cursor.execute(sql, data)
                    connection.commit()
                    close_connection_to_db(connection)
