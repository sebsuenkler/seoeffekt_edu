#script to check the number of canonical links

#include libs
import sys
sys.path.insert(0, '..')
from include import *

def canonical(hash, tree):

    xpath = '//a[@rel="canonical"] | //link[@rel="canonical"]'
    module = 'check canonical'
    counter = 0

    res = tree.xpath(xpath)

    for r in res:
        counter = counter + 1

    value = str(counter)

    check_evaluations_result(hash, module, value)
