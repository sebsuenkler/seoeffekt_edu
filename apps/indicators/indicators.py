#main app to collect technical seo indicators from a webpage

#include libs
import sys
sys.path.insert(0, '..')
from include import *

#apps for seo indicators
from https import https

from micro import micros

from og import og

from viewport import viewport

from sitemap import sitemap

from wordpress import wordpress

from canonical import canonical

from nofollow import nofollow

from h1 import h1

from keywords import kw

from kw_in_url import kw_in_url

from description import description

from title import title

from title_h1 import title_h1

from links import links

from keyword_density import keyword_density

from plugins import plugins

from sources import sources

from robots import robots

from url_length import url_length

from identical_title import identical_title

try:

    def get_result_hashes():
        if update == "0":
            hashes = Evaluations.getResultHashesNoUpdate(number_indicators)
        else:
            hashes = Evaluations.getResultHashes()
        return hashes

    def get_result_source(hash):
        try:
            source = Results.getResultsSource(hash)
            html_source = Helpers.html_unescape(source[0][1])
            soup = BeautifulSoup(html_source, 'lxml')
            html_source = soup.get_text().strip()
            html_source = html_source.split('\n')
            html_source = set(html_source)
            html_source = list(html_source)
            html_comments = Helpers.html_unescape(source[0][2])
            html_comments = html_comments.split("[comment_source]")
            html_comments = set(html_comments)
            html_comments = list(html_comments)
            code = Helpers.html_unescape(source[0][0])
            code = code.lower()
            tree = html.fromstring(code)
            source_array = [code, tree, html_source, html_comments, soup]
            return source_array
        except:
            return False

    def get_result_meta(hash):
        meta = Results.getRecentResultByHash(hash)
        return meta

    def get_result_query(meta):
        results_id = meta[0][-1]
        query_row = Queries.getQuerybyResult(results_id)
        try:
            query = query_row[0][0]
            query = query.lower()
            return query
        except:
            return False

    #create url list
    hashes = get_result_hashes()
    random.shuffle(hashes)

    #analyze every url from list
    for h in hashes:
        print(h)
        hash = h


        result_source = get_result_source(hash)

        if result_source:

            code = result_source[0]
            tree = result_source[1]
            html_source = result_source[2]
            html_comments = result_source[3]
            soup = result_source[4]

            #call functions
            meta = get_result_meta(hash)
            for m in meta:
                result_id = m[0]
                main_hash = m[6]
                result_url = m[10]
                result_main = m[11]

            query = get_result_query(meta)

            if query:
                check_query = True
            else:
                query = "-1"
                check_query = False

            #print('canonical')
            canonical(hash, tree)

            #print('kw')
            kw(hash,tree, query, check_query)
            kw_in_url(hash,result_url, query, check_query)
            keyword_density(hash,query, soup, check_query)

            #print('title_h1')
            title_h1(hash,tree)

            #print('viewport')
            viewport(hash,code)

            #print('description')
            description(hash,tree)

            #print('title')
            title(hash,tree)

            #print('links')
            links(hash,result_main, html_source)

            #print('plugins')
            plugins(hash,html_source, html_comments)

            #print('https')
            https(result_url, hash)

            #print('micros')
            micros(hash,html_comments, html_source)

            #print('og')
            og(hash,code)

            #print('sitemap')
            sitemap(hash,code)

            #print('wordpress')
            wordpress(hash,tree)

            #print('nofollow')
            nofollow(hash,tree)

            #print('h1')
            h1(hash,tree)

            #print('sources')
            sources(hash, result_url, result_main)

            #print('robots')
            robots(hash, result_main, main_hash)

            #print('url_length')
            url_length(hash, result_url)

            #print('identical_title')
            identical_title(hash, result_main)


except Exception as e:
    print(e)
