#script to check title tag in html

#include libs

import sys
sys.path.insert(0, '..')
from include import *

today = date.today()

def title(hash, tree):
    xpath_title = "//title/text()"
    xpath_meta_title = "//meta[@name='title']/@content"
    xpath_og_title = "//meta[@property='og:title']/@content"
    module = 'check title'

    value = '0'

    check_title = str(tree.xpath(xpath_title))
    check_meta_title = str(tree.xpath(xpath_meta_title))
    check_og_title = str(tree.xpath(xpath_og_title))

    if len(check_title) > 2 or len(check_meta_title) > 2  or len(check_og_title) > 2:
        value = '1'

    check_evaluations_result(hash, module, value)
