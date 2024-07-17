import fnmatch
from urllib.parse import urlparse
import csv
import json
from lxml import html
from bs4 import BeautifulSoup

from lib.sources import *

def match_text(text, pattern):
    text = text.lower()
    pattern= pattern.lower()
    check = fnmatch.fnmatch(text, pattern)
    return check

def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    except:
        return False

def get_scheme(url):
    parsed = urlparse(url)
    return parsed.scheme

def get_netloc(url):
    parsed = urlparse(url)
    return parsed.netloc

def get_plugins():

    with open('config/evaluation.ini', 'r') as f:
        array = json.load(f)

    plugins_json = array["text-match"]
    plugins = []

    for get_plugin in plugins_json:
        name = get_plugin
        source = plugins_json[name]["source"]
        with open(source, 'r') as csvfile:
            csv_result = csv.reader(csvfile, delimiter=',', quotechar='"')
            source = list(csv_result)
        plugin = {
        "name": name,
        "source": source
        }
        plugins.append(plugin)

    return plugins

def get_sources():
    with open('config/sources.ini', 'r') as f:
        array = json.load(f)

    sources_json = array["text-match"]
    sources = []

    for get_source in sources_json:
        name = get_source
        source = sources_json[name]["source"]
        with open(source, 'r') as csvfile:
            csv_result = csv.reader(csvfile, delimiter=',', quotechar='"')
            source = list(csv_result)
        load_url = {
        "name": name,
        "source": source
        }
        sources.append(load_url)

    return sources


def identify_url_length(url):
    result = -1
    url = url.replace("www.", "")

    if (match_text(url, "https://*")):
        url = url.replace("https://", "")

    elif(match_text(url, "http://*")):
        url = url.replace("http://", "")

    result = str(len(url))

    return result

def identify_https(url):
    scheme = get_scheme(url)
    result = 0

    if scheme == 'https':
        result = 1

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

    pattern = '<*meta*og:*>'
    result = 0

    if match_text(source, pattern):
        result = 1

    return result

def identify_viewport(source):

    pattern = '*meta*name*viewport*'
    result = 0

    if match_text(source, pattern):
        result = 1

    return result

def identify_sitemap(source):

    pattern = "*a*href*sitemap*"
    result = 0

    if (match_text(source, pattern)):
        result = 1

    return result

def identify_wordpress(source):
    tree = html.fromstring(source)
    xpath = "//meta[@name='generator']/@content"
    content = tree.xpath(xpath)
    check = str(content)
    check = check.lower()

    result = 0

    if len(check) > 1:
        pattern = "*wordpress*"
        if match_text(check, pattern):
            result = 1

    return result

def identify_canonical(source):
    tree = html.fromstring(source)
    xpath = '//a[@rel="canonical"] | //link[@rel="canonical"]'
    hyperlink_counter = 0

    hyperlinks = tree.xpath(xpath)

    for hyperlink in hyperlinks:
        hyperlink_counter = hyperlink_counter + 1

    return hyperlink_counter

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

    return hyperlink_counter

def identify_h1(source):
    tree = html.fromstring(source)
    xpath = "//h1/text()"
    counter = 0
    res = tree.xpath(xpath)

    for r in res:
        counter = counter + 1

    return counter


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

    return counter


def identify_keywords_in_url(url, search_query):

        counter = 0

        keywords = search_query.split()

        for kw in keywords:
            if kw.lower() in url.lower():
                counter = counter + 1

        return counter


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

        return kw_density

def identify_description(source):

    source = source.lower()

    tree = html.fromstring(source)

    result = 0

    xpath_meta = "//meta[@name='description']/@content"
    xpath_og_property = "//meta[@property='og:description']/@content"
    xpath_og_name = "//meta[@name='og:description']/@content"
    xpath_site_description = "//p[@class='site-description']/text()"

    meta_content = str(tree.xpath(xpath_meta))
    og_property_content = str(tree.xpath(xpath_og_property))
    og_name = str(tree.xpath(xpath_og_name))
    site_description = str(tree.xpath(xpath_site_description))

    if(len(meta_content) > 5 or len(og_property_content) > 5 or len(og_name) > 5 or len(site_description) > 5):
        result = 1

    return result

def identify_title(source):
    source = source.lower()
    tree = html.fromstring(source)
    result = 0
    xpath_title = "//title/text()"
    xpath_meta_title = "//meta[@name='title']/@content"
    xpath_og_title = "//meta[@property='og:title']/@content"
    xpath_site_title = "//p[@class='site-title']/text()"

    check_title = str(tree.xpath(xpath_title))
    check_meta_title = str(tree.xpath(xpath_meta_title))
    check_og_title = str(tree.xpath(xpath_og_title))
    site_title = str(tree.xpath(xpath_site_title))

    if len(check_title) > 2 or len(check_meta_title) > 2  or len(check_og_title) > 2 or len(site_title) > 2:
        result = 1

    return result

def identify_hyperlinks(hyperlinks, main):
    link = ""
    internal_links = 0
    external_links = 0
    i = 0
    e = 0
    link_list = list()

    urls_split = hyperlinks.split("[url]")

    for u in urls_split:

        link_split = u.split("   ")
        link = (link_split[-1])
        link_list.append(link)
    link_list.sort()

    for href in link_list:
        if is_valid_url(href):
            if main in href:
                internal_links = internal_links + 1
            else:
                external_links = external_links + 1

    i = internal_links
    e = external_links

    hyper_links_counter = {'internal': i, 'external': e}

    return hyper_links_counter

def identify_plugins(source):

    soup = BeautifulSoup(source, 'lxml')
    source_split = soup.get_text().strip()
    source_split = source_split.split('\n')
    source_split = set(source_split)
    source_split = list(source_split)

    plugins = get_plugins()
    found_plugins = {}

    for plugin in plugins:
        plugin_type = plugin['name']
        plugin_list = plugin['source']
        plugin_names = []

        for get_plugin in plugin_list:
            plugin_name = get_plugin[0]
            plugin_search_pattern = get_plugin[1]

            for section in source_split:
                if match_text(section, plugin_search_pattern):
                    plugin_names.append(plugin_name)

            update = {plugin_type:plugin_names}
            found_plugins.update(update)

    return found_plugins

def identify_sources(main):
    sources = get_sources()
    found_urls = {}

    main = main.replace('www.', '')

    for source in sources:
        source_type = source['name']
        source_list = source['source']
        source_urls = []

        for get_source in source_list:
            source_url = get_source[0]
            if get_netloc(source_url):
                source_url = get_netloc(source_url)
            source_url = source_url.replace('www.', '')

            if source_url in main:
                source_urls.append(source_url)

            update = {source_type:source_urls}
            found_urls.update(update)

    return found_urls

def identify_robots_txt(main):
    robots_url = main+'robots.txt'
    result = 0

    try:
        source = save_robot_txt(robots_url)

        if source:
            source = decode_source(source)

            pattern = "*crawl-delay*"
            if match_text(source, pattern):
                result = 1

            pattern = "*user agent*"
            if match_text(source, pattern):
                result = 1

            pattern = "*user-agent*"
            if match_text(source, pattern):
                result = 1

            pattern = "*sitemap*"
            if match_text(source, pattern):
                result = 1

            pattern = "*noindex*"
            if match_text(source, pattern):
                result = 1

            pattern = "*seo*"
            if match_text(source, pattern):
                result = 1

    except:
        result = -1

    return result

def identify_loading_time(url):

    driver = Driver(
            browser="chrome",
            wire=True,
            uc=True,
            headless2=True,
            incognito=False,
            agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            do_not_track=True,
            undetectable=True,
            extension_dir=ext_path,
            locale_code="de",
            no_sandbox=True,
            )    
    driver.set_page_load_timeout(120)
    loading_time = -1

    try:
        driver.get(url)
        time.sleep(5)
        ''' Use Navigation Timing  API to calculate the timings that matter the most '''
        navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
        responseStart = driver.execute_script("return window.performance.timing.responseStart")
        domComplete = driver.execute_script("return window.performance.timing.domComplete")
        loadStart = driver.execute_script("return window.performance.timing.domInteractive")
        EventEnd = driver.execute_script("return window.performance.timing.loadEventEnd")
        ''' Calculate the performance'''
        backendPerformance_calc = responseStart - navigationStart
        frontendPerformance_calc = domComplete - responseStart
        loadingTime = EventEnd - navigationStart
        loading_time = loadingTime / 1000
        driver.quit()
    except Exception as e:
        print(str(e))
        pass

    driver.quit()

    return loading_time

