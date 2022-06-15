#script to check open graph tags

#include libs

import sys
sys.path.insert(0, '..')
from include import *

today = date.today()

def og(hash, code):
    module = 'check og'
    pattern = '*og:*'
    value = '0'

    if Helpers.matchText(code, pattern):
        value = '1'


    check_evaluations_result(hash, module, value)
