import base64
from datetime import date


today = date.today()

from urllib.parse import urlsplit
from urllib.parse import urlparse
import socket

from lxml import html
from bs4 import BeautifulSoup
import fnmatch

from lib.identify_indicators import *



import datetime

from lib.sources import *
from log import *
from db import *


def classify_result(source, url, query, result_id):

    def match_text(text, pattern):
        text = text.lower()
        pattern= pattern.lower()
        check = fnmatch.fnmatch(text, pattern)
        return check

    def check_progress_classification():
        connection = connect_to_db()
        cursor = connection.cursor()
        dup = False
        data = cursor.execute("SELECT result_id FROM EVALUATION WHERE result_id = ? LIMIT 1",(result_id,))
        connection.commit()
        for row in data:
            dup = row
        close_connection_to_db(connection)
        if not dup:
            return True
        else:
            return False

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

    meta = get_meta(url)



    def get_hyperlinks(source, main = meta[1]):
        hyperlinks = ""

        if source !="error":
            #extract all comments in source code
            soup = BeautifulSoup(source, 'lxml')

            soup_urls = []
            tags = soup.find_all('a')

            for tag in tags:
                hyperlink_text = str(tag.string).strip()
                href = str(tag.get('href')).strip()
                if "http" not in href:
                    href = href.lstrip('/')
                    href = main+href

                hyperlink = "[url]"+hyperlink_text+"   "+href
                if not match_text(hyperlink, '*mailto:*'):
                    if hyperlink and hyperlink != " ":
                        hyperlinks = hyperlinks+hyperlink

            return hyperlinks



    def check_classification_dup(result_id):
        connection = connect_to_db()
        cursor = connection.cursor()
        dup = False
        data = cursor.execute("SELECT result_id FROM CLASSIFICATION WHERE result_id = ?",(result_id,))
        connection.commit()
        for row in data:
            dup = row
        close_connection_to_db(connection)
        if not dup:
            return True
        else:
            return False

    def check_insert_result_dup(module):
        connection = connect_to_db()
        cursor = connection.cursor()
        dup = False
        data = cursor.execute("SELECT result_id FROM EVALUATION WHERE result_id = ? AND module = ?",(result_id, module,))
        connection.commit()
        for row in data:
            dup = row
        close_connection_to_db(connection)
        if not dup:
            return True
        else:
            return False

    def insert_results(module, insert_result):
        connection = connect_to_db()
        cursor = connection.cursor()
        sql = 'INSERT INTO EVALUATION(result_id, module, value, date) values(?,?,?,?)'
        data = (result_id, module, insert_result, today)
        cursor.execute(sql, data)
        connection.commit()
        close_connection_to_db(connection)

    if check_progress_classification():

        if source !="error":

            hyperlinks = get_hyperlinks(source)

            indicators = {}

            indicators['url_length'] = identify_url_length(url)
            indicators['https'] = identify_https(url)

            indicators['micros'] = identify_micros(source)
            indicators['og'] = identify_og(source)
            indicators['viewport'] = identify_viewport(source)
            indicators['sitemap'] = identify_sitemap(source)
            indicators['wordpress'] = identify_wordpress(source)
            indicators['canonical'] = identify_canonical(source)
            indicators['nofollow'] = identify_nofollow(source)
            indicators['h1'] = identify_h1(source)

            indicators['keywords_in_source'] = -1
            indicators['keywords_in_url'] = -1
            indicators['keyword_density'] = -1

            if query:
                indicators['keywords_in_source'] = identify_keywords_in_source(source, query)
                indicators['keywords_in_url'] = identify_keywords_in_url(url, query)
                indicators['keyword_density'] = identify_keyword_density(source, query)

            indicators['description'] = identify_description(source)
            indicators['title'] = identify_title(source)

            indicators['hyperlinks'] = identify_hyperlinks(hyperlinks, meta[1])

            indicators['plugins'] = identify_plugins(source)

            indicators['sources'] = identify_sources(meta[1])

            indicators['robots_txt'] = identify_robots_txt(meta[1])

            indicators['loading_time'] = identify_loading_time(url)

    


            for key, value in indicators.items():

                if type(value) != list and type(value) is not dict:
                    module = key
                    insert_result = str(value)

                    if check_insert_result_dup(module):
                        insert_results(module, insert_result)
                else:
                    if (type(value) is list):
                        module = key
                        insert_result = ", ".join(value)

                        if check_insert_result_dup(module):
                            insert_results(module, insert_result)

                    if (type(value) is dict):
                        for k, v in value.items():
                            module = k
                            insert_result = v
                            if (type(v) is list):
                                insert_result = ", ".join(v)
                            else:
                                insert_result = str(v)

                            if check_insert_result_dup(module):
                                insert_results(module, insert_result)



            #translate the dictionary into variables
            url_length = indicators['url_length']
            https = indicators['https']
            micros = len(indicators['micros'])
            og = indicators['og']
            viewport = indicators['viewport']
            sitemap = indicators['sitemap']
            wordpress = indicators['wordpress']
            canonical = indicators['canonical']
            nofollow = indicators['nofollow']
            h1 = indicators['h1']

            keywords_in_source = indicators['keywords_in_source']
            keywords_in_url = indicators['keywords_in_url']
            keyword_density = indicators['keyword_density']

            description = indicators['description']
            title = indicators['title']

            internal_links = indicators['hyperlinks']['internal']
            external_links = indicators['hyperlinks']['external']

            tools_analytics = len(indicators['plugins']['tools analytics'])
            tools_seo = len(indicators['plugins']['tools seo'])
            tools_caching = len(indicators['plugins']['tools caching'])
            tools_social = len(indicators['plugins']['tools social'])
            tools_ads = len(indicators['plugins']['tools ads'])

            sources_ads = len(indicators['sources']['ads'])
            sources_company = len(indicators['sources']['company'])
            sources_customers = len(indicators['sources']['seo_customers'])
            sources_news = len(indicators['sources']['news'])
            sources_not_optimized = len(indicators['sources']['not_optimized'])
            sources_services = len(indicators['sources']['search_engine_services'])
            sources_shops = len(indicators['sources']['shops'])

            robots_txt = indicators['robots_txt']
            loading_time = indicators['loading_time']

            #classify the result
            optimized = 0
            probably_optimized = 0
            probably_not_optimized = 0
            classification_result = "uncertain"

            #most probably optimized
            if tools_seo > 0 or sources_customers > 0 or sources_news > 0 or sources_ads > 0 or micros > 0:
                optimized = 1
                classification_result = 'most_probably_optimized'

            #probably optimized
            if optimized == 0 and (tools_analytics > 0 or sources_shops > 0 or sources_company > 0 or viewport == 1 or robots_txt == 1 or sitemap == 1 or nofollow > 0 or canonical > 0 or (loading_time < 3 and loading_time > 0)):
                probably_optimized = 1
                classification_result = 'probably_optimized'

            #probably_not_optimized
            if (title == 0 or description == 0 or loading_time > 30) and og == 0:
                classification_result = 'probably_not_optimized'

            if sources_not_optimized > 0:
                classification_result = 'most_probably_not_optimized'

        if source == "error":
            classification_result = "error"

        if check_classification_dup(result_id):
            connection = connect_to_db()
            cursor = connection.cursor()
            sql = 'INSERT INTO CLASSIFICATION(result_id, classification, value, date) values(?,?,?,?)'
            data = (result_id, 'rule_based', classification_result, today)
            cursor.execute(sql, data)
            connection.commit()
            close_connection_to_db(connection)


connection = connect_to_db()
cursor = connection.cursor()
source_results = cursor.execute("SELECT source, url, query, SOURCE.result_id  FROM SOURCE, SEARCH_RESULT, QUERY WHERE SOURCE.result_id = SEARCH_RESULT.id AND SEARCH_RESULT.query_id = QUERY.id AND progress = 1 AND SOURCE.result_id = SEARCH_RESULT.id AND SOURCE.result_id NOT IN (SELECT CLASSIFICATION.result_id FROM CLASSIFICATION) AND SOURCE.source IS NOT NULL ORDER BY RANDOM() LIMIT 5")
connection.commit()

for s in source_results:
    source = s[0]
    if source != "error":
        try:
            source = decode_source(s[0])
        except:
            source = "error"

    url = s[1]
    query = s[2]
    result_id = s[3]

    timestamp = datetime.datetime.now()
    timestamp = timestamp.strftime("%d-%m-%Y, %H:%M:%S")

    write_to_log(timestamp, "Classify "+str(url))


    classify_result(source, url, query, result_id)
close_connection_to_db(connection)
