#sys libs
#include libs
import sys
sys.path.insert(0, '..')
from include import *

#tool libs


with open('../../config/global_vars.ini', 'r') as f:
    array = json.load(f)


today = date.today()


def save_content(url, hash, main):

    if(not Results.getSource(hash)):
        Results.insertSource(hash, "0", "0", "0", today, 0)

    try:
        source = Results.saveResult(url)

        if source == 'error':
            Results.updateSources(hash, "-1", "-1", "-1", date.today(), 1)
        else:
            content = Results.getContent(source, main)
            Results.updateSources(hash, content[0], content[1], content[2], date.today(), 1)

    except:
        Results.updateSources(hash, "-1", "-1", "-1", date.today(), 1)
        pass


def get_results():
    results = Results.getResultsSourcesNULL()
    return results


def insert_sources(results):
    counter = 0
    for result in results:
        counter = counter + 1

        hash = result[0]
        main_hash = result[1]
        url = result[2]
        main = result[3]
        #print(hash)
        #noch datumsprüfung umsetzen....
        if(not Results.getRecentSource(hash)):
            print(url)
            print(hash)
            save_content(url, hash, main)

results = get_results()
print(results)


insert_sources(results)
