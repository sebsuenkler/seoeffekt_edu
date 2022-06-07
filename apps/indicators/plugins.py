#script to check seo plugins and analytics tools in html code

#include libs

import sys
sys.path.insert(0, '..')
from include import *

today = date.today()

def get_tools():

    with open('../../config/evaluation.ini', 'r') as f:
        array = json.load(f)

    text_match_json = array["text-match"]
    text_match_tools = []
    i = -1


    for text_match in text_match_json:
        i+=1
        name = text_match
        source = text_match_json[text_match]["source"]
        with open(source, 'r') as csvfile:
            csv_result = csv.reader(csvfile, delimiter=',', quotechar='"')
            source = list(csv_result)
        tool = {
        "name": name,
        "source": source
        }
        text_match_tools.append(tool)

    return text_match_tools


def plugins(hash, html_source, html_comments):
    tools = get_tools()

    for text_match_tool in tools:
        plugins = []
        module = text_match_tool["name"]
        matches = text_match_tool["source"]
        value = '0'

        module_count = text_match_tool["name"] + ' count'
        count_value = '0'


        check_evaluations_result(hash, module, value)


        check_evaluations_result(hash, module_count, count_value)

        for check in matches:
            obj = check[0]
            pattern = check[1]
            for comment in html_comments:
                if(len(comment) < 3000):
                    if Helpers.matchText(comment, pattern):
                        plugins.append([module, obj])


        for check in matches:
            obj = check[0]
            pattern = check[1]
            for snip in html_source:
                if(len(snip) < 3000):
                    if Helpers.matchText(snip, pattern):
                        plugins.append([module, obj])


        plugins = Helpers.remove_duplicates_from_list(plugins)

        if(len(plugins) > 0):
            plug = ""
            for p in plugins:
                plug = plug+p[1]+'###'
            value = plug[:-3]
            count_value = str(len(plugins))
            Evaluations.UpdateEvaluationResult(value, today, hash, module)
            Evaluations.UpdateEvaluationResult(count_value, today, hash, module_count)
