#script to check if domain is in one of the sources lists with categorized domains

#include libs

import sys
sys.path.insert(0, '..')
from include import *

def sources(hash, result_url, result_main):

    sources_categories = ['source ads', 'source company', 'source known', 'source news', 'source not optimized', 'source search engine', 'source shop', 'source top']

    def get_netloc(url):
        parsed = urlparse(url)
        return parsed.netloc

    for source_category in sources_categories:

        def get_sources(source_category):
            sources_file = '../../evaluations/'+source_category+'.csv'
            sources = []
            sources_loc = []
            with open(sources_file, 'r') as csvfile:
                urls = csv.reader(csvfile)

                for u in urls:
                    sources.append(u)

            for s in sources:
                s_url = s[0]
                netloc = get_netloc(s_url)
                if(netloc):
                    sources_loc.append(netloc)

            return sources_loc

        sources = get_sources(source_category)

        result_url = result_url.replace('www.', '')
        result_main = result_main.replace('www.', '')

        module = source_category

        value = '0'

        check_evaluations_result(hash, module, value)

        for s in sources:
            s = s.replace('www.', '')
            if s in result_url or s in result_main:
                value = '1'
                Evaluations.UpdateEvaluationResult(value, today, hash, module)
