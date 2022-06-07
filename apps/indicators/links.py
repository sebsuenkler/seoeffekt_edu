#script count internal and external links

#include libs

import sys
sys.path.insert(0, '..')
from include import *

today = date.today()

def is_valid(url):
    try:
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    except:
        return False

def links(hash, result_main, html_source):
    link = ""
    internal_links = 0
    external_links = 0
    i = '0'
    e = '0'
    link_list = list()
    urls = html_source[0]
    urls_split = urls.split("[url]")

    for u in urls_split:

        link_split = u.split("   ")
        link = (link_split[-1])
        link_list.append(link)
    link_list.sort()

    for href in link_list:
        if is_valid(href):
            if result_main in href:
                internal_links = internal_links + 1
            else:
                external_links = external_links + 1

    i = str(internal_links)
    e = str(external_links)


    module = 'check internal links'
    value = i

    check_evaluations_result(hash, module, value)


    module = 'check external links'
    value = e

    check_evaluations_result(hash, module, value)
