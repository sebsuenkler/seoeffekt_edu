#script check keywords in url

#include libs

import sys
sys.path.insert(0, '..')
from include import *

today = date.today()

def kw_in_url(hash, result_url, query, check_query):
        url = result_url.lower()
        module = 'check kw_in_url'
        value = '0'

        if check_query:
            pattern = '*'+query+'*'
            if (Helpers.matchText(url, pattern)):
                value = '1'

        check_evaluations_result(hash, module, value)
