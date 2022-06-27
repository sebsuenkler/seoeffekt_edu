import sqlite3 as sl

connection = sl.connect('seo_effect.db')

cursor=connection.cursor()

scraper_id = 0

with connection:
    data = cursor.execute("SELECT * FROM SCRAPER WHERE progress =? ORDER BY RANDOM() LIMIT 1", (0,))
    for row in data:
        scraper_id = row[0]
        study_id = row[1]
        query_id = row[2]
        query = row[3]
        search_engine = row[4]

if scraper_id != 0:

    with connection:
        cursor.execute("UPDATE SCRAPER SET progress =? WHERE id =?", (2,scraper_id,))
        connection.commit()


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
        urls = tree.xpath(xpath_results)
        return urls

    def check_captcha(driver):
        source = driver.page_source
        if captcha in source:
            return True
        else:
            return False

    def check_max_results(driver):
        source = driver.page_source
        if max_results_filter in source:
            return True
        else:
            return False


    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    driver.install_addon(extension_path, temporary=False)
    driver.get(search_url)
    time.sleep(3)
    search = driver.find_element(By.NAME, search_box)
    search.send_keys(query)
    search.send_keys(Keys.RETURN)
    time.sleep(3)

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

                next_page = driver.find_element(By.XPATH, xpath_next_page.format(p))

                next_page.click()

                time.sleep(3)

                urls = get_search_results(driver)
                search_results.append(urls)

            else:
                print("max_results")
                pass
    else:
        blocked = True

    #driver.quit()

    if blocked:
        with connection:
            cursor.execute("UPDATE SCRAPER SET progress =? WHERE id =?", (-1,scraper_id,))
            connection.commit()
    else:
        with connection:
            cursor.execute("UPDATE SCRAPER SET progress =? WHERE id =?", (1,scraper_id,))
            connection.commit()

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

                sql = 'INSERT INTO SEARCH_RESULT(study_id, query_id, scraper_id, ip, search_engine, position, url, main_url, timestamp, date) values(?,?,?,?,?,?,?,?,?,?)'
                data = (study_id, query_id, scraper_id, ip, search_engine, position, url, main_url, timestamp, today)
                cursor.execute(sql, data)
                connection.commit()
                result_id = cursor.lastrowid

                sql = 'INSERT INTO SOURCE(result_id, progress, date) values(?,?,?)'
                data = (result_id, 0, today)
                cursor.execute(sql, data)
                connection.commit()
