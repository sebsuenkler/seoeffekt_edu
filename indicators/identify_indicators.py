import fnmatch
from urllib.parse import urlparse
import csv
import json
from lxml import html
from bs4 import BeautifulSoup

def match_text(text, pattern):
    text = text.lower()
    pattern= pattern.lower()
    check = fnmatch.fnmatch(text, pattern)
    return check

def get_scheme(url):
    parsed = urlparse(url)
    return parsed.scheme

def identify_url_length(url):
    result = '-1'
    url = url.replace("www.", "")

    if (match_text(url, "https://*")):
        url = url.replace("https://", "")

    elif(match_text(url, "http://*")):
        url = url.replace("http://", "")

    result = str(len(url))

    return result

def identify_https(url):
    scheme = get_scheme(url)
    result = '0'

    if scheme == 'https':
        result = '1'

    return result

def identify_micros(source):
    micros_list = []
    with open('lists/micro.csv', 'r') as csvfile:
        micros = csv.reader(csvfile)
        for m in micros:
            module = m[0]
            pattern = m[1]
            item = (module, pattern)
            micros_list.append(item)

    micros_found = []

    for ms in micros_list:
        obj = ms[0]
        pattern = ms[1]
        for s in source:
            if(len(s) < 3000):
                if match_text(s, pattern):
                    micros_found.append([obj])

    return micros_found


def identify_og(source):

    pattern = '*og:*'
    result = '0'

    if match_text(source, pattern):
        result = '1'

    return result

def identify_viewport(source):

    pattern = '*meta*name*viewport*'
    result = '0'

    if match_text(source, pattern):
        result = '1'

    return result

def identify_sitemap(source):

    pattern = "*sitemap*"
    result = '0'

    if (match_text(source, pattern)):
        result = '1'

    return result

def identify_wordpress(source):
    tree = html.fromstring(source)
    xpath = "//meta[@name='generator']/@content"
    content = tree.xpath(xpath)
    check = str(content)
    check = check.lower()

    result = '0'

    if len(check) > 1:
        pattern = "*wordpress*"
        if match_text(check, pattern):
            result = '1'

    return result

def identify_canonical(source):
    tree = html.fromstring(source)
    xpath = '//a[@rel="canonical"] | //link[@rel="canonical"]'
    hyperlink_counter = 0

    hyperlinks = tree.xpath(xpath)

    for hyperlink in hyperlinks:
        hyperlink_counter = hyperlink_counter + 1

    return str(hyperlink_counter)

def identify_nofollow(source):
    tree = html.fromstring(source)
    xpath_code = '//a[@rel="nofollow"]'
    hyperlink_counter = 0

    hyperlinks_code = tree.xpath(xpath_code)

    for hyperlink in hyperlinks_code:
        hyperlink_counter = hyperlink_counter + 1

    xpath_robot = '/meta[@name="robots"]/@content'

    hyperlinks_robot = tree.xpath(xpath_robot)

    for hyperlink in hyperlinks_robot:
        if hyperlink == 'nofollow':
            hyperlink_counter = hyperlink_counter + 1

    return str(hyperlink_counter)

def identify_h1(source):
    tree = html.fromstring(source)
    xpath = "//h1/text()"
    counter = 0
    res = tree.xpath(xpath)

    for r in res:
        counter = counter + 1

    return str(counter)


def identify_keywords_in_source(source, search_query):

    counter = 0

    keywords = search_query.split()

    tree = html.fromstring(source)

    with open('config/kw.ini', 'r') as f:
        array = json.load(f)

    kw_array = array['keywords']

    for kw in keywords:

        for key, xpath in kw_array.items():
            content = tree.xpath(xpath)

            for c in content:
                if kw.lower() in c.lower():
                    counter = counter + 1

    return str(counter)


def identify_keywords_in_url(url, search_query):

        counter = 0

        keywords = search_query.split()

        for kw in keywords:
            if kw.lower() in url.lower():
                counter = counter + 1

        return str(counter)


def identify_keyword_density(source, search_query):

    soup = BeautifulSoup(source, 'lxml')

    w_counter = 0
    kw_counter = 0
    kw_density = 0

    if search_query:

        query_split = search_query.split()
        q_patterns = []
        for q in query_split:
            q_patterns.append('*'+q+'*')

        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text()

        lines = (line.strip() for line in text.splitlines())

        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ''.join(chunk for chunk in chunks if chunk)

        text = ' '.join(text.split())

        source_list = text.split(' ')

        w_counter = len(source_list)

        kw_counter = 0

        for q in q_patterns:

            for w in source_list:
                if match_text(w, q):
                    kw_counter = kw_counter + 1

        kw_density = kw_counter / w_counter * 100
        decimals=0
        multiplier = 10 ** decimals
        kw_density = int(kw_density * multiplier) / multiplier

        return str(kw_density)

def identify_description(source):

    tree = html.fromstring(source)

    result = '0'

    xpath_meta = "//meta[@name='description']/@content"
    xpath_og_property = "//meta[@property='og:description']/@content"
    xpath_og_name = "//meta[@name='og:description']/@content"
    xpath_site_description = "//p[@class='site-description']/text()"

    meta_content = str(tree.xpath(xpath_meta))
    og_property_content = str(tree.xpath(xpath_og_property))
    og_name = str(tree.xpath(xpath_og_name))
    site_description = str(tree.xpath(xpath_site_description))

    if(len(meta_content) > 5 or len(og_property_content) > 5 or len(og_name) > 5 or len(site_description) > 5):
        result = '1'

    return result

def identify_title(source):
    tree = html.fromstring(source)
    result = '0'
    xpath_title = "//title/text()"
    xpath_meta_title = "//meta[@name='title']/@content"
    xpath_og_title = "//meta[@property='og:title']/@content"
    xpath_site_title = "//p[@class='site-title']/text()"

    check_title = str(tree.xpath(xpath_title))
    check_meta_title = str(tree.xpath(xpath_meta_title))
    check_og_title = str(tree.xpath(xpath_og_title))
    site_title = str(tree.xpath(xpath_site_title))

    if len(check_title) > 2 or len(check_meta_title) > 2  or len(check_og_title) > 2 or len(site_title) > 2:
        result = '1'

    return result
