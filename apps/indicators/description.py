#script to check for description

#include libs
import sys
sys.path.insert(0, '..')
from include import *

today = date.today()

def description(hash, tree):

    xpath_meta = "//meta[@name='description']/@content"
    xpath_og_property = "//meta[@property='og:description']/@content"
    xpath_og_name = "//meta[@name='og:description']/@content"
    module = 'check description'
    value = '0'

    meta_content = str(tree.xpath(xpath_meta))
    og_property_content = str(tree.xpath(xpath_og_property))
    og_name = str(tree.xpath(xpath_og_name))

    if(len(meta_content) > 5 or len(og_property_content) > 5 or len(og_name) > 5):
        value = '1'

    check_evaluations_result(hash, module, value)
