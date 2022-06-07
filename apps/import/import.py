#sys libs
#include libs
import sys
sys.path.insert(0, '..')
from include import *

file = "../../evaluations/source known.csv"

study_id = 9

query_id = 0

scrapers_id = 0

search_engine = "Import"

results_position = 0

results_import = 1

job_id = 0

today = date.today()

timestamp = datetime.now()



with open(file, 'r') as csvfile:
    csv_result = csv.reader(csvfile, delimiter=',', quotechar='"')
    source = list(csv_result)

for url in source:

    url = url[0]

    check_url = Results.getURL(query_id, study_id, url, search_engine)
    if (not check_url):

        url_meta = Results.getResultMeta(url)
        hash = url_meta[0]
        ip = url_meta[1]
        main = url_meta[2]
        main_hash = Helpers.computeMD5hash(main)
        contact_url = "0"
        contact_hash = "0"
        contact_url = "0"

        Results.insertResult(query_id, study_id, job_id, results_import, ip, hash, main_hash, contact_hash, search_engine, url, main, contact_url, today, timestamp, 1, results_position)

        check_sources = Results.getSource(hash)
        if not check_sources:
            Results.insertSource(hash, None, None, None, today, 0)
