#script to count keywords

#include libs

import sys
sys.path.insert(0, '..')
from include import *

#open config file with possible keyword positions in a document
with open('../../config/kw.ini', 'r') as f:
    array = json.load(f)

kw_array = array['keywords']

today = date.today()

def kw(hash, tree, query, check_query):
    kw = array['keywords']

    for k, v in kw.items():
        key = k
        counter = 0
        xpath = v
        content = tree.xpath(xpath)

        if check_query:
            pattern = '*'+query+'*'
            for c in content:
                if (Helpers.matchText(c, pattern)):
                    counter = counter + 1

        module = key
        value = str(counter)

        check_evaluations_result(hash, module, value)
