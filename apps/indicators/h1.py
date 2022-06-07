#script to check h1 headings

#include libs
import sys
sys.path.insert(0, '..')
from include import *


def h1(hash, tree):

    xpath = "//h1/text()"
    module = 'check h1'
    counter = 0
    value = '0'

    res = tree.xpath(xpath)

    for r in res:
        counter = counter + 1

    if counter > 0:
        value = '1'

    check_evaluations_result(hash, module, value)
