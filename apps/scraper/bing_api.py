#script to scraper bing api

#include libs
import sys
sys.path.insert(0, '..')
from include import *


def generate_scraping_job(query, scraper):

    query_string = query[1]
    query_id = query[4]
    study_id = query[0]
    search_engine = scraper
    result_pages = 20
    number_multi = 50
    check_jobs = Scrapers.getScrapingJobs(query_id, study_id, search_engine)
    if not check_jobs:

        for r in range(result_pages):
            start = r * number_multi
            print(start)

            try:
                Scrapers.insertScrapingJobs(query_id, study_id, query_string, search_engine, start, date.today())
                print('Scraper Job: '+query_string+' SE:'+search_engine+' start:'+str(start)+' created')
            except:
                break;



def scrape_query(query, scraper):

    today = date.today()
    jobs = Scrapers.getScrapingJobsByQueryProgressSE(query, 0, scraper)


    subscription_key = "b175056d732742038339a83743658448"
    assert subscription_key

    search_url = "https://api.bing.microsoft.com/v7.0/search"

    for job in jobs:

        search_engine = job[3]
        search_query = job[2]
        start = job[4]
        query_id = job[0]
        study_id = job[1]
        job_id = job[7]

        progress = 2

        Scrapers.updateScrapingJobQuerySearchEngine(query_id, search_engine, progress)

        sleeper = random.randint(3,10)

        time.sleep(sleeper)


        #headers = {"Ocp-Apim-Subscription-Key": subscription_key, "X-Search-ClientIP":"217.111.88.182"}
        headers = {"Ocp-Apim-Subscription-Key": subscription_key}
        params = {"q": search_query, "textDecorations": True, "textFormat": "HTML", "count": 50, "offset": start, "responseFilter": "Webpages"}

        try:
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            search_results = response.json()
            web_results = search_results['webPages']


        except:
            Helpers.saveLog("../../logs/"+str(study_id)+"_"+search_query+".log", 'Error Scraping Job', 1)
            Scrapers.updateScrapingJobQuerySearchEngine(query_id, search_engine, -1)
            Results.deleteResultsNoScrapers(query_id, search_engine)
            exit()


        results = []

        for w in web_results['value']:
            results.append(w['url'])


        if results:

            results_check = results[-1]

            check_url = Results.getURL(query_id, study_id, results_check, search_engine)

            if check_url:
                Scrapers.updateScrapingJobQuerySearchEngine(query_id, search_engine, 1)
                Helpers.saveLog("../../logs/"+str(study_id)+"_"+search_query+".log", 'Max Results', 1)
                exit()


            else:
                Scrapers.updateScrapingJob(job_id, 1)
                Helpers.saveLog("../../logs/"+str(study_id)+"_"+search_query+".log", 'Start Scraping Results', 1)

                results_position = 1

                for result in results:

                    url = result

                    check_url = Results.getURL(query_id, study_id, url, search_engine)

                    if (not check_url):

                        url_meta = Results.getResultMeta(url, str(study_id), search_engine, str(query_id))
                        hash = url_meta[0]
                        ip = url_meta[1]
                        main = url_meta[2]
                        main_hash = Helpers.computeMD5hash(main+str(study_id)+search_engine+str(query_id))
                        contact_url = "0"
                        Helpers.saveLog("../../logs/"+str(study_id)+"_"+search_query+".log", url, 1)
                        contact_hash = "0"
                        contact_url = "0"


                        last_position = Results.getLastPosition(query_id, study_id, search_engine, today)

                        if last_position:
                            results_position = last_position[0][0] + 1


                            if Results.getPosition(query_id, study_id, search_engine, results_position):
                                results_position = results_position + 1


                        Results.insertResult(query_id, study_id, job_id, 0, ip, hash, main_hash, contact_hash, search_engine, url, main, contact_url, today, datetime.now(), 1, results_position)

                        check_sources = Results.getSource(hash)
                        if not check_sources:
                            Results.insertSource(hash, None, None, None, today, 0)

                        Helpers.saveLog("../../logs/"+str(study_id)+"_"+search_query+".log", 'Insert Result', 1)



studies = Studies.getStudiesScraper()

for s in studies:
    if "Bing_API" in s[-1]:
        scraper = "Bing_API"

        studies_id = s[-3]
        queries = Queries.getQueriesStudy(studies_id)

        for q in queries:
            query_id = q[-2]

            job = 0
            check_jobs = Scrapers.getScrapingJobsBySE(query_id, scraper)
            count_jobs = check_jobs[0][0]
            if count_jobs == 0:
                job = 1

            if job == 1:
                generate_scraping_job(q, scraper)

        open_queries = Queries.getOpenQueriesStudybySE(studies_id, scraper)

        if open_queries:
            random.shuffle(open_queries)
            o = open_queries[0]


            if o:
                check_progress = Scrapers.getScrapingJobsByQueryProgressSE(o, 2, scraper)
                if not check_progress:
                    print(o)
                    scrape_query(o, scraper)
