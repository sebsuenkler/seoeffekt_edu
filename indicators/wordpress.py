#script to check wordpress

#include libs

import sys
sys.path.insert(0, '..')
from include import *

today = date.today()

def wordpress(hash, tree):
    xpath = "//meta[@name='generator']/@content"
    module = 'check wordpress'
    content = tree.xpath(xpath)
    check = str(content)
    check = check.lower()

    value = '0'

    if len(check) > 1:
        pattern = "*wordpress*"
        if Helpers.matchText(check, pattern):
            value = '1'

    check_evaluations_result(hash, module, value)
