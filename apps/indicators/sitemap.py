#script to check sitemap

#include libs

import sys
sys.path.insert(0, '..')
from include import *

today = date.today()

def sitemap(hash, code):
    pattern = "*sitemap*"
    module = 'check sitemap'
    value = '0'
    sitemap_counter = 0

    if (Helpers.matchText(code, pattern)):
        sitemap_counter = sitemap_counter + 1

    if sitemap_counter > 0:
        value = '1'
    else:
        value = '0'

    check_evaluations_result(hash, module, value)
