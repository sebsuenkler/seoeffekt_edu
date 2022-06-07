#script to calculate url url length

#include libs

import sys
sys.path.insert(0, '..')
from include import *

def url_length(hash, result_url):

    value = '-1'
    module = 'check url_length'



    result_url = result_url.replace("www.", "")

    url = result_url

    if (Helpers.matchText(result_url, "https://*")):
        url = result_url.replace("https://", "")

    elif(Helpers.matchText(result_url, "http://*")):
        url = result_url.replace("http://", "")


    value = str(len(url))

    check_evaluations_result(hash, module, value)
