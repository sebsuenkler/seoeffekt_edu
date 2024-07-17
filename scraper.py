
import os
import inspect

from pathlib import Path

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

parentdir = os.path.dirname(currentdir)

ext_path = currentdir+"/i_care_about_cookies_unpacked"

import datetime

import json

import importlib

from lib.sources import get_real_url

from db import *
from log import *

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

        import time

        from seleniumbase import Driver

        from lxml import html
        from bs4 import BeautifulSoup

        import json

        with open('scraper.json') as json_file:
            search_engines_json = json.load(json_file)

        try:

            scraper_lib = search_engines_json[search_engine]['scraper_file']
            limit = search_engines_json[search_engine]['limit']
            scraper = importlib.import_module(scraper_lib)


            search_results = scraper.run(query, limit)

            if search_results == -1:
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

                        if position <= limit:

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
        except:
            connection = connect_to_db()
            cursor = connection.cursor()
            cursor.execute("UPDATE SCRAPER SET progress =? WHERE id =?", (-1,scraper_id,))
            connection.commit()
            close_connection_to_db(connection)

            timestamp = datetime.datetime.now()
            timestamp = timestamp.strftime("%d-%m-%Y, %H:%M:%S")

            write_to_log(timestamp, "Scrape "+str(search_engine)+" Job_Id:"+str(scraper_id)+" Query:"+str(query)+" failed")
