#Class for scrapers table
class Scrapers:
    def __init__(self, cursor):
        self.cursor = cursor

#read from db

#read all scaping jobs by progress
    def getScrapingJobsByProgress(cursor, progress):
        sql= "SELECT * from scrapers WHERE scrapers_progress=%s ORDER BY RANDOM()"
        data = (progress)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows

#read all scaping jobs by progress
    def getScrapingJobsByProgressSE(cursor, progress, se):
        sql= "SELECT * from scrapers WHERE scrapers_progress=%s AND scrapers_se =%s ORDER BY RANDOM()"
        data = (progress, se)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows

#read scaping jobs by progress and query
    def getScrapingJobsByQueryProgress(cursor, query_id, progress):
        sql= "SELECT * FROM scrapers WHERE scrapers_queries_id = %s AND scrapers_progress = %s ORDER BY scrapers_start, scrapers_se ASC"
        data = (query_id, progress)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows


    def getScrapingJobsByQueryProgressSE(cursor, query_id, progress, se):
        sql= "SELECT * FROM scrapers WHERE scrapers_queries_id = %s AND scrapers_progress = %s AND scrapers_se = %s ORDER BY scrapers_start, scrapers_se"
        data = (query_id, progress, se)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows

#read scraping jobs by query
    def getScrapingJobsByQuery(cursor, query_id):
        sql= "SELECT * FROM scrapers WHERE scrapers_queries_id = %s ORDER BY scrapers_id"
        data = (query_id)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows

#read scraping jobs by Search Engine
    def getScrapingJobsBySE(cursor, query_id, search_engine):
        sql= "SELECT count(scrapers_id) FROM scrapers WHERE scrapers_queries_id = %s AND scrapers_se =%s"
        data = (query_id, search_engine)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows

    def getScrapingJobsByStudyQueries(cursor, study):
        sql= "SELECT count(distinct(scrapers_queries_id)) from scrapers, queries WHERE scrapers_queries_id = queries_id AND scrapers_studies_id=%s"
        data = (study)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows

#write to db

#generate scraping joby by queries
    def insertScrapingJobs(cursor, query_id, study_id, query_string, search_engine, start, today):
        cursor.execute(
            "INSERT INTO scrapers (scrapers_queries_id, scrapers_studies_id, scrapers_queries_query, scrapers_se, scrapers_start, scrapers_date, scrapers_progress) VALUES (%s, %s, %s, %s, %s, %s, %s);", # remove parenthesis here, which ends the execute call
            (query_id, study_id, query_string, search_engine, start, today, 0)
        )

#update status of scraping job
    def updateScrapingJob(cursor, job_id, progress):
        cursor.execute(
            "UPDATE scrapers SET scrapers_progress = %s WHERE scrapers_id = %s",
            (progress, job_id)
        )

#update status of scraping job by query; important for queries with a limited range of search results
    def updateScrapingJobQuery(cursor, query_id, progress):
        cursor.execute(
            "UPDATE scrapers SET scrapers_progress = %s WHERE scrapers_queries_id = %s",
            (progress, query_id)
        )

#update status of scraping job by query; important for queries with a limited range of search results
    def updateScrapingJobQuerySeJobId(cursor, query_id, progress, se, job_id):
        cursor.execute(
            "UPDATE scrapers SET scrapers_progress = %s WHERE scrapers_queries_id = %s AND scrapers_se = %s AND scrapers_id >= %s",
            (progress, query_id, se, job_id)
        )


#update scraping job by query and search engine
    def updateScrapingJobQuerySearchEngine(cursor, query_id, search_engine, progress):
        cursor.execute(
            "UPDATE scrapers SET scrapers_progress = %s WHERE scrapers_queries_id = %s AND scrapers_se =%s",
            (progress, query_id, search_engine)
        )

#reset scraper_jobs

    def resetScrapingJobs(cursor):

        cursor.execute(
            "DELETE FROM scrapers WHERE scrapers_progress = -1"
        )


    def getScrapingJobs(cursor, query_id, study_id, search_engine):
        sql= "SELECT scrapers_id FROM scrapers WHERE scrapers_queries_id = %s AND scrapers_studies_id =%s AND scrapers_se = %s"
        data = (query_id, study_id, search_engine)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows
