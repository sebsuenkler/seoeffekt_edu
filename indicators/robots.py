#script to check seo in robots.txt

#include libs

import sys
sys.path.insert(0, '..')
from include import *

def robots(hash, result_main, main_hash):

    #print("robots")


    def get_results_main_hash(main_hash):
        hashes = Results.getResultHashesOnMain(main_hash)
        return hashes


    robots_url = result_main+'robots.txt'

    module = 'robots_txt'

    res_hashes = get_results_main_hash(main_hash)

    if (not Evaluations.getEvaluationModule(hash, module)):

        try:
            source = Results.saveResult(robots_url)
            s = source.lower()

            #print(s)

            value = '0'


            p = "*crawl-delay*"
            if Helpers.matchText(s, p):
                value = '1'

            p = "*user agent*"
            if Helpers.matchText(s, p):
                value = '1'


            p = "*user-agent:*"
            if Helpers.matchText(s, p):
                value = '1'

            p = "*sitemap*"
            if Helpers.matchText(s, p):
                value = '1'

            p = "*noindex*"
            if Helpers.matchText(s, p):
                value = '1'

            p = "*seo*"
            if Helpers.matchText(s, p):
                value = '1'

        except:
            value  = '-1'

        Evaluations.insertEvaluationResult(hash, module, value, today)

        for r_h in res_hashes:

            if (not Evaluations.getEvaluationModuleResult(r_h, module, value)):
                #print(r_h)
                #print(robots_url)
                Evaluations.insertEvaluationResult(r_h, module, value, today)
