# Rule-based Classifier

#include libs

import sys
sys.path.insert(0, '..')
from include import *


#function to classify

def classify(classifier_id, hashes):


    #functions to check the usage of titles in the document

    for h in hashes:

        hash = h[0]
        results_url = h[1]
        results_main = h[2]
        results_speed = h[3]

        evaluations_results = Evaluations.getEvaluationsResults(hash)

        dict_results = {}

        for e in evaluations_results:
            evaluations_module =  e[0]
            evaluations_result = e[1]

            #indicators for rule based classification
            dict_results.update({evaluations_module: evaluations_result})

        
        #convert dict elements for rule based classification

        #sources:
        source_not_optimized = int(dict_results['source not optimized'])
        source_news = int(dict_results['source news'])
        source_known = int(dict_results['source known'])
        source_search_engine = int(dict_results['source search engine'])
        source_shop = int(dict_results['source shop'])
        source_top = int(dict_results['source top'])
        source_ads = int(dict_results['source ads'])
        source_company = int(dict_results['source company'])

        #indicators:
        indicator_https = int(dict_results['check https'])
        indicator_robots_txt = int(dict_results['robots_txt'])
        indicator_sitemap = int(dict_results['check sitemap'])
        indicator_nofollow = int(dict_results['check nofollow'])
        indicator_speed = float(results_speed)
        indicator_canonical = int(dict_results['check canonical'])
        indicator_viewport = int(dict_results['check viewport'])
        indicator_og = int(dict_results['check og'])
        indicator_micros = int(dict_results['micros counter'])
        indicator_title = int(dict_results['check title'])
        indicator_identical_title = int(dict_results['check identical title'])
        indicator_description = int(dict_results['check description'])
        indicator_speed = results_speed

        #plugins and tools
        tools_analytics = int(dict_results['tools analytics count'])
        tools_seo = int(dict_results['tools seo count'])
        tools_caching = int(dict_results['tools caching count'])
        tools_content = int(dict_results['tools content count'])
        tools_social = int(dict_results['tools social count'])
        tools_ads = int(dict_results['tools ads count'])

        #classification
        not_optimized = 0
        optimized = 0
        probably_optimized = 0
        probably_not_optimized = 0
        classification_result = "uncertain"

        #most_probably_not_optimized
        if source_not_optimized == 1:
            not_optimized = 1
            classification_result = 'not optimized'

        #most probably optimized
        if not_optimized == 0 and (tools_seo > 0 or source_known == 1 or source_news == 1 or source_ads == 1 or indicator_micros > 0):
            optimized = 1
            classification_result = 'optimized'


        #probably optimized
        if optimized == 0 and not_optimized == 0 and (tools_analytics > 0 or source_shop == 1 or source_company == 1 or indicator_viewport == 1 or indicator_robots_txt == 1 or indicator_sitemap == 1 or indicator_nofollow > 0 or indicator_canonical > 0 or (indicator_speed < 3 and indicator_speed > 0)):
            probably_optimized = 1
            classification_result = 'probably_optimized'


        #probably_not_optimized
        if optimized == 0 and not_optimized == 0 and (indicator_title == 0 or indicator_description == 0 or indicator_speed > 60):
                probably_not_optimized = 1
                classification_result = 'probably_not_optimized'


        if '.pdf' in results_url:
            classification_result = 'PDF'

        Evaluations.updateClassificationResult(hash, classification_result, classifier_id, today)

        print(results_url)
        print(hash)
        print(classification_result)
