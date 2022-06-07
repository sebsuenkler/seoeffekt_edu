#script to check title tags in headers

#include libs

import sys
sys.path.insert(0, '..')
from include import *

today = date.today()

def title_h1(hash, tree):

    xpath_title = "//title/text()"
    xpath_meta_title = "//meta[@name='title']/@content"
    xpath_og_title = "//meta[@property='og:title']/@content"
    xpath_h1 = "//h1/text()"
    module = 'check title'
    value = '0'

    title = tree.xpath(xpath_title)
    check_title = str(title)
    check_title = check_title.lower()
    check_title = check_title.strip()
    check_title = Helpers.html_escape(check_title)

    meta_title = tree.xpath(xpath_meta_title)
    check_meta_title = str(meta_title)
    check_meta_title = check_meta_title.lower()
    check_meta_title = check_meta_title.strip()
    check_meta_title = Helpers.html_escape(check_meta_title)

    og_title = tree.xpath(xpath_og_title)
    check_og_title = str(og_title)
    check_og_title = check_og_title.lower()
    check_og_title = check_og_title.strip()
    check_og_title = Helpers.html_escape(check_og_title)

    h1 = tree.xpath(xpath_h1)

    ct_value_counter = 0
    ct_value = '0'
    ct_module = 'check title_h1_identical'



    check_evaluations_result(hash, ct_module, ct_value)

    cth_value_counter = 0
    cth_value = '0'

    cth_module = 'check title_h1_match'


    check_evaluations_result(hash, cth_module, cth_value)

    for h in h1:
        h = str(h)
        h = h.lower()
        h = h.strip()
        h = Helpers.html_escape(h)
        check_title = re.sub('\W+',' ', check_title)
        check_meta_title = re.sub('\W+',' ', check_meta_title)
        check_og_title = re.sub('\W+',' ', check_og_title)
        h = re.sub('\W+',' ', h)

        if check_title == h or check_meta_title == h or check_og_title == h:
            ct_value_counter = ct_value_counter + 1

        ct_value = str(ct_value_counter)

        Evaluations.UpdateEvaluationResult(ct_value, today, hash, ct_module)


        pattern = '*'+check_title+'*'
        if (Helpers.matchText(h, pattern)):
            cth_value_counter = cth_value_counter + 1

        pattern = '*'+check_meta_title+'*'
        if (Helpers.matchText(h, pattern)):
            cth_value_counter = cth_value_counter + 1

        pattern = '*'+check_og_title+'*'
        if (Helpers.matchText(h, pattern)):
            cth_value_counter = cth_value_counter + 1


        cth_value = str(cth_value_counter)


        Evaluations.UpdateEvaluationResult(cth_value, today, hash, cth_module)
