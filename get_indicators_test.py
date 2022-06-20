def match_text(text, pattern):
    text = text.lower()
    pattern= pattern.lower()
    check = fnmatch.fnmatch(text, pattern)
    return check

import sqlite3 as sl

connection = sl.connect('seo_effect.db')

cursor=connection.cursor()

with connection:
    source_results = cursor.execute("SELECT source, url FROM SOURCE WHERE hash = 1")
    for s in source_results:
        source = s[0]
        url = s[1]

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

meta = get_meta(url)

from lxml import html
from bs4 import BeautifulSoup
import fnmatch

def get_hyperlinks(source, main = meta[1]):
    hyperlinks = ""

    if (source !="error"):
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

hyperlinks = get_hyperlinks(source)

indicators = {}

from indicators import identify_indicators

source = '<li class="nav-item mt-3 linklist__entry "> <a href="/sitemap/"class="nav-link font-weight-light py-0 pr-2 linklist__link">    Sitemap </a>'

indicators['url_length'] = identify_indicators.identify_url_length(url)
indicators['https'] = identify_indicators.identify_https(url)

indicators['micros'] = identify_indicators.identify_micros(source)
indicators['og'] = identify_indicators.identify_og(source)
indicators['viewport'] = identify_indicators.identify_viewport(source)
indicators['sitemap'] = identify_indicators.identify_sitemap(source)
indicators['wordpress'] = identify_indicators.identify_wordpress(source)
indicators['canonical'] = identify_indicators.identify_canonical(source)
indicators['nofollow'] = identify_indicators.identify_nofollow(source)
indicators['h1'] = identify_indicators.identify_h1(source)


query = "stahlschlag industrial"

indicators['keywords_in_source'] = identify_indicators.identify_keywords_in_source(source, query)
indicators['keywords_in_url'] = identify_indicators.identify_keywords_in_url(url, query)
indicators['keyword_density'] = identify_indicators.identify_keyword_density(source, query)

indicators['description'] = identify_indicators.identify_description(source)
indicators['title'] = identify_indicators.identify_title(source)


print(indicators)




# #main app to collect technical seo indicators from a webpage
#
# #include libs
# import sys
# sys.path.insert(0, '..')
# from include import *
#
# #apps for seo indicators
# from https import https
#
# from micro import micros
#
# from og import og
#
# from viewport import viewport
#
# from sitemap import sitemap
#
# from wordpress import wordpress
#
# from canonical import canonical
#
# from nofollow import nofollow
#
# from h1 import h1
#
# from keywords import kw
#
# from kw_in_url import kw_in_url
#
# from description import description
#
# from title import title
#
# from title_h1 import title_h1
#
# from links import links
#
# from keyword_density import keyword_density
#
# from plugins import plugins
#
# from sources import sources
#
# from robots import robots
#
# from url_length import url_length
#
# from identical_title import identical_title
#
# try:
#
#     def get_result_hashes():
#         if update == "0":
#             hashes = Evaluations.getResultHashesNoUpdate(number_indicators)
#         else:
#             hashes = Evaluations.getResultHashes()
#         return hashes
#
#     def get_result_source(hash):
#         try:
#             source = Results.getResultsSource(hash)
#             html_source = Helpers.html_unescape(source[0][1])
#             soup = BeautifulSoup(html_source, 'lxml')
#             html_source = soup.get_text().strip()
#             html_source = html_source.split('\n')
#             html_source = set(html_source)
#             html_source = list(html_source)
#             html_comments = Helpers.html_unescape(source[0][2])
#             html_comments = html_comments.split("[comment_source]")
#             html_comments = set(html_comments)
#             html_comments = list(html_comments)
#             code = Helpers.html_unescape(source[0][0])
#             code = code.lower()
#             tree = html.fromstring(code)
#             source_array = [code, tree, html_source, html_comments, soup]
#             return source_array
#         except:
#             return False
#
#     def get_result_meta(hash):
#         meta = Results.getRecentResultByHash(hash)
#         return meta
#
#     def get_result_query(meta):
#         results_id = meta[0][-1]
#         query_row = Queries.getQuerybyResult(results_id)
#         try:
#             query = query_row[0][0]
#             query = query.lower()
#             return query
#         except:
#             return False
#
#     #create url list
#     hashes = get_result_hashes()
#     random.shuffle(hashes)
#
#     #analyze every url from list
#     for h in hashes:
#         print(h)
#         hash = h
#
#
#         result_source = get_result_source(hash)
#
#         if result_source:
#
#             code = result_source[0]
#             tree = result_source[1]
#             html_source = result_source[2]
#             html_comments = result_source[3]
#             soup = result_source[4]
#
#             #call functions
#             meta = get_result_meta(hash)
#             for m in meta:
#                 result_id = m[0]
#                 main_hash = m[6]
#                 result_url = m[10]
#                 result_main = m[11]
#
#             query = get_result_query(meta)
#
#             if query:
#                 check_query = True
#             else:
#                 query = "-1"
#                 check_query = False
#
#             #print('canonical')
#             canonical(hash, tree)
#
#             #print('kw')
#             kw(hash,tree, query, check_query)
#             kw_in_url(hash,result_url, query, check_query)
#             keyword_density(hash,query, soup, check_query)
#
#             #print('title_h1')
#             title_h1(hash,tree)
#
#             #print('viewport')
#             viewport(hash,code)
#
#             #print('description')
#             description(hash,tree)
#
#             #print('title')
#             title(hash,tree)
#
#             #print('links')
#             links(hash,result_main, html_source)
#
#             #print('plugins')
#             plugins(hash,html_source, html_comments)
#
#             #print('https')
#             https(result_url, hash)
#
#             #print('micros')
#             micros(hash,html_comments, html_source)
#
#             #print('og')
#             og(hash,code)
#
#             #print('sitemap')
#             sitemap(hash,code)
#
#             #print('wordpress')
#             wordpress(hash,tree)
#
#             #print('nofollow')
#             nofollow(hash,tree)
#
#             #print('h1')
#             h1(hash,tree)
#
#             #print('sources')
#             sources(hash, result_url, result_main)
#
#             #print('robots')
#             robots(hash, result_main, main_hash)
#
#             #print('url_length')
#             url_length(hash, result_url)
#
#             #print('identical_title')
#             identical_title(hash, result_main)
#
#
# except Exception as e:
#     print(e)
