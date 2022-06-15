#script to calculate keyword_density

#include libs
import sys
sys.path.insert(0, '..')
from include import *

today = date.today()

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def keyword_density(hash, query, soup, check_query):

    w_counter = 0
    kw_counter = 0
    kw_density = 0

    if check_query:

        query_split = query.split()
        q_patterns = []
        for q in query_split:
            q_patterns.append('*'+q+'*')

            # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

            # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = ''.join(chunk for chunk in chunks if chunk)

        text = ' '.join(text.split())

        source_list = text.split(' ')

        w_counter = len(source_list)

        kw_counter = 0

        for q in q_patterns:
            for w in source_list:
                if Helpers.matchText(w, q):
                    kw_counter = kw_counter + 1

        kw_density = kw_counter / w_counter * 100

        kw_density = truncate(kw_density, 3)

    kw_counter_v = str(kw_counter)
    w_counter_v = str(w_counter)
    kw_density_v = str(kw_density)

    module = "check kw_count"
    value = kw_counter_v

    check_evaluations_result(hash, module, value)


    module = "check word_count"
    value = w_counter_v

    check_evaluations_result(hash, module, value)


    module = "check kw_density"
    value = kw_density_v

    check_evaluations_result(hash, module, value)
