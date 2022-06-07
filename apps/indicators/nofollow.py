#script to check nofollow links

#include libs

import sys
sys.path.insert(0, '..')
from include import *

today = date.today()

def nofollow(hash, tree):

    xpath = '//a[@rel="nofollow"]'
    module = 'check nofollow'
    counter = 0

    res1 = tree.xpath(xpath)

    for r in res1:
        counter = counter + 1


    xpath_2 = '/meta[@name="robots"]/@content'

    res2 = tree.xpath(xpath_2)

    for r in res2:
        if r == 'nofollow':
            counter = counter + 1

    value = str(counter)

    check_evaluations_result(hash, module, value)
