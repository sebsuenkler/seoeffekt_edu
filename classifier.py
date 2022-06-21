from get_indicators import get_indicators
query = "stahlschlag"
hash = "1"
indicators = get_indicators(hash, query)

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
not_optimized = 0
optimized = 0
probably_optimized = 0
probably_not_optimized = 0
classification_result = "uncertain"

if sources_not_optimized > 0:
    not_optimized = 1
    classification_result = 'most_probably_not_optimized'

#most probably optimized
if not_optimized == 0 and (tools_seo > 0 or sources_customers > 0 or sources_news > 0 or sources_ads > 0 or micros > 0):
    optimized = 1
    classification_result = 'most_probably_optimized'

#probably optimized
if optimized == 0 and not_optimized == 0 and (tools_analytics > 0 or sources_shops > 0 or sources_company > 0 or viewport == 1 or robots_txt == 1 or sitemap == 1 or nofollow > 0 or canonical > 0 or (loading_time < 3 and loading_time > 0)):
    probably_optimized = 1
    classification_result = 'probably_optimized'

#probably_not_optimized
if title == 0 or description == 0 or loading_time > 30:
    classification_result = 'probably_not_optimized'

for key, value in indicators.items():
    if type(value) is int or type(value) is float:
        value = str(value)
    if type(value) is list:
        print(key)
        values = "0"
        if value:
            for v in value:
                values = ""
                if v:
                    values = values + v + ";"

        print(values)
    if type(value) is dict:
        for k, v in value.items():
            key = k
            if v:
                value = str(v)
            else:
                value = '0'
            print(key)
            print(value)
