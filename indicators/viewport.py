#script to check the viewport

#include libs

import sys
sys.path.insert(0, '..')
from include import *

today = date.today()

def viewport(hash, code):
    module = 'check viewport'
    pattern = '*meta*name*viewport*'
    value = '0'

    if Helpers.matchText(code, pattern):
        value = '1'

    check_evaluations_result(hash, module, value)
