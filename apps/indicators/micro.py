#script to check micro data

#include libs

import sys
sys.path.insert(0, '..')
from include import *

micro_file = '../../evaluations/micro.csv'

today = date.today()

def get_micros():
    micros_list = []
    with open(micro_file, 'r') as csvfile:
        micros = csv.reader(csvfile)
        for m in micros:
            modul = m[0]
            pattern = m[1]
            item = (modul, pattern)
            micros_list.append(item)
    return micros_list


def micros(hash, html_comments, html_source):
    micros_list = get_micros()
    micros_save = []


    for ms in micros_list:
        obj = ms[0]
        pattern = ms[1]

        for comment in html_comments:
            if(len(comment) < 3000):
                if Helpers.matchText(comment, pattern):
                    micros_save.append([obj])
        for s in html_source:
            if(len(s) < 3000):
                if Helpers.matchText(s, pattern):
                    micros_save.append([obj])

    micros_save = Helpers.remove_duplicates_from_list(micros_save)

    res = ''

    if(len(micros_save) == 0):
        module = 'micros'
        value = '0'

        check_evaluations_result(hash, module, value)

        module = 'micros counter'
        value = '0'

        check_evaluations_result(hash, module, value)

    else:
        for m in micros_save:
            res = '#'+res+m[0]

        module = 'micros'

        check_evaluations_result(hash, module, res)


        module = 'micros counter'
        value = len(micros_save)
        value = str(value)

        check_evaluations_result(hash, module, value)
