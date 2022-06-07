#done!!!
#sys libs
import sys
sys.path.insert(0, '..')
from include import *


with open('../../config/global_vars.ini', 'r') as f:
    array = json.load(f)

#app funcs

def get_studies():
    studies = Studies.getStudiesScraper()
    return studies

def get_open_jobs_queries(study_id):
    queries = Queries.getOpenQueriesStudy(study_id)
    return queries

def get_queries(study_id):
    #get all queries from study
    queries = Queries.getQueriesNoScrapers(study_id)
    return queries


def generate_scraping_job(query, scraper):
    print(query)
    query_string = query[1]
    query_id = query[4]
    study_id = query[0]
    number_multi = int(scraper.number_multi)
    number_div = int(scraper.number_div)
    result_pages = int(scraper.results_range/number_multi)
    search_engine = scraper.search_engine
    start_add = int(scraper.start_add)
    check_jobs = Scrapers.getScrapingJobs(query_id, study_id, search_engine)
    if not check_jobs:
        for i in range(result_pages):
            if start_add > 0:
                i = i + start_add
            start = int(i * number_multi / number_div)
            try:
                Scrapers.insertScrapingJobs(query_id, study_id, query_string, search_engine, (start * number_div), date.today())
                print('Scraper Job: '+query_string+' SE:'+search_engine+' start:'+str(start)+' created')
            except:
                break;






def scrape_query(query, scraper):



    today = date.today()
    jobs = Scrapers.getScrapingJobsByQueryProgressSE(query, 0, scraper.search_engine)


    for job in jobs:

        search_engine = job[3]
        search_query = job[2]
        search_query = search_query.replace(' ', '+')
        start = job[4]
        query_id = job[0]
        study_id = job[1]
        job_id = job[7]

        print(start)

        progress = 2

        Scrapers.updateScrapingJobQuerySearchEngine(query_id, search_engine, progress)

        Helpers.saveLog("../../logs/"+str(study_id)+"_"+search_query+search_engine+".log", "Start Scraping", 1)
        built_query = scraper.search_url+search_query+scraper.start+str(start)+scraper.language+scraper.number_parameter
        Helpers.saveLog("../../logs/"+str(study_id)+"_"+search_query+search_engine+".log", built_query, 1)

        res = Scrapers.scrapeQuery(built_query, scraper.xpath, start, scraper.filter)

        if res:
            results = res[0]
            source = res[1]
            print(results)

            if (results == 'filtered'):
                Scrapers.updateScrapingJobQuerySearchEngine(query_id, search_engine, 1)
                Helpers.saveLog("../../logs/"+str(study_id)+"_"+search_query+".log", 'Max Results', 1)
                exit()

            else:
                Scrapers.updateScrapingJob(job_id, 1)
                Helpers.saveLog("../../logs/"+str(study_id)+"_"+search_query+".log", 'Start Scraping Results', 1)

                if scraper.serp_filter != "":
                    tree = html.fromstring(source)
                    serp_element = tree.xpath(scraper.serp_filter)
                    serp = Helpers.html_escape(source)
                    if serp_element:
                        check_serp = Results.getSERP(query_id)
                        if not check_serp:
                            Results.insertSERP(query_id, serp, 1, today)



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
        else:
            Helpers.saveLog("../../logs/"+str(study_id)+"_"+search_query+".log", 'Error Scraping Job', 1)
            Scrapers.updateScrapingJobQuerySearchEngine(query_id, search_engine, -1)
            Results.deleteResultsNoScrapers(query_id, search_engine)
            exit()




#app controller

try:
    #if not(Scrapers.getScrapingJobsByProgress(-1)):



    scrapers = Scrapers.generateScrapers()

    studies = get_studies()



    for s in studies:



        to_scrape = []
        study_id = s[-3]


        studies_scrapers = s[-1]


        if studies_scrapers:


            if ";" in studies_scrapers:
                studies_scrapers = studies_scrapers.split(";")

                for sc in studies_scrapers:
                    to_scrape.append(sc)
            else:
                to_scrape.append(studies_scrapers)

            for ts in to_scrape:


                if ts !="Bing_API" and ts !="Google_Selenium" and ts !="Google_Selenium_SV":

                    queries = get_queries(study_id)


                    for q in queries:
                        query_db = Queries.getQuerybyID(q)
                        query_id = query_db[0][-2]

                        job = 0
                        check_jobs = Scrapers.getScrapingJobsBySE(query_id, ts)
                        count_jobs = check_jobs[0][0]
                        if count_jobs == 0:
                            job = 1

                        if job == 1:
                            for s in scrapers:
                                if s.search_engine == ts:
                                    generate_scraping_job(query_db[0], s)



                        o = []

                        #open queries prüfen der anzahl der jobs anhand der möglichen anzahl an jobs, nicht scrapen, wenn nicht alle jobs bereits erstellt sind; abhängig von der maximalen anzahl berechnet aus max results und result pages bzw. einfach vom der start position des letzten jobs

                        if not(Scrapers.getScrapingJobsByProgressSE(-1, ts)):

                            open_queries = Queries.getOpenQueriesStudybySE(study_id, ts)



                            if open_queries:
                                random.shuffle(open_queries)
                                o = open_queries[0]



                            if o:
                                for s in scrapers:
                                    if s.search_engine == ts:
                                        check_error = Scrapers.getScrapingJobsByQueryProgressSE(o, -1, ts)
                                        check_progress = Scrapers.getScrapingJobsByQueryProgressSE(o, 2, ts)
                                        if not check_error and not check_progress:
                                            print(o)
                                            scrape_query(o, s)









except Exception as e:
    print(e)
