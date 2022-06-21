def get_indicators(hash, query):

    def match_text(text, pattern):
        text = text.lower()
        pattern= pattern.lower()
        check = fnmatch.fnmatch(text, pattern)
        return check

    import sqlite3 as sl

    connection = sl.connect('seo_effect.db')

    cursor=connection.cursor()

    with connection:
        source_results = cursor.execute("SELECT source, url FROM SOURCE WHERE hash = ?",(hash,))
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

    indicators['keywords_in_source'] = -1
    indicators['keywords_in_url'] = -1
    indicators['keyword_density'] = -1

    if query:
        indicators['keywords_in_source'] = identify_indicators.identify_keywords_in_source(source, query)
        indicators['keywords_in_url'] = identify_indicators.identify_keywords_in_url(url, query)
        indicators['keyword_density'] = identify_indicators.identify_keyword_density(source, query)

    indicators['description'] = identify_indicators.identify_description(source)
    indicators['title'] = identify_indicators.identify_title(source)

    indicators['hyperlinks'] = identify_indicators.identify_hyperlinks(hyperlinks, meta[1])

    indicators['plugins'] = identify_indicators.identify_plugins(source)

    indicators['sources'] = identify_indicators.identify_sources(meta[1])

    indicators['robots_txt'] = identify_indicators.identify_robots_txt(meta[1])

    indicators['loading_time'] = identify_indicators.identify_loading_time(url)

    return indicators
