#Class for results table

class Results:

    def __init__(self, cursor):
        self.cursor = cursor

    def getURL(cursor, query_id, study_id, results_url, results_se):
        sql= "select results_id from results where results_queries_id = %s AND results_studies_id= %s AND results_url = %s AND results_se = %s LIMIT 1"
        data = (query_id, study_id, results_url, results_se)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows

    def getLastPosition(cursor, query_id, study_id, results_se, today):
        sql= "select results_position from results where results_queries_id = %s AND results_studies_id	= %s AND results_se = %s AND results_date = %s ORDER BY results_id DESC LIMIT 1"
        data = (query_id, study_id, results_se, today)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows


    def getPosition(cursor, query_id, study_id, search_engine, results_position):
        sql= "select results_position from results where results_queries_id = %s AND results_studies_id	= %s AND results_se = %s AND results_position = %s ORDER BY results_id DESC LIMIT 1"
        data = (query_id, study_id, search_engine, results_position)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows



    def insertResult(cursor, query_id, study_id, job_id, upload, ip, hash, main_hash, contact_hash, search_engine, url, main, contact, today, timestamp, progress, results_position):
        cursor.execute(
            "INSERT INTO results (results_queries_id, results_studies_id, results_scrapers_id, results_import, results_ip, results_hash, results_main_hash, results_contact_hash, results_se, results_url, results_main, results_contact, results_date, results_timestamp, results_progress, results_position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;", # remove parenthesis here, which ends the execute call
            (query_id, study_id, job_id, upload, ip, hash, main_hash, contact_hash, search_engine, url, main, contact, today, timestamp, progress, results_position,)
        )

    def insertSource(cursor, hash, source, urls, comments, date, progress):
        cursor.execute(
            "INSERT INTO sources (sources_hash, sources_source, sources_urls, sources_comments, sources_date, sources_progress) VALUES (%s, %s, %s, %s, %s, %s);",
            (hash, source, urls, comments, date, progress,)
        )



    def updateSources(cursor, hash, source, urls, comments, date, progress):
        try:
            cursor.execute(
                "UPDATE sources SET sources_source = %s, sources_urls = %s, sources_comments = %s, sources_date = %s, sources_progress = %s WHERE sources_hash = %s",
                (source, urls, comments, date, progress, hash,)
            )
        except:
            print("exit_error")
            cursor.execute(
                "UPDATE sources SET sources_source = %s, sources_urls = %s, sources_comments = %s, sources_date = %s, sources_progress = %s WHERE sources_hash = %s",
                ("-1", "-1", "-1", date, progress, hash,)
            )

    def insertSpeed(cursor, hash, speed):
        cursor.execute(
            "UPDATE sources SET sources_speed = %s WHERE sources_hash = %s",
            (speed, hash,)
        )

    def getSpeed(cursor, hash):
        sql= "SELECT sources_speed FROM sources WHERE sources_hash = %s LIMIT 1"
        data = (hash,)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows

    def getSource(cursor, hash):
        sql= "SELECT sources_id from sources WHERE sources_hash=%s LIMIT 1"
        data = (hash,)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows

    def getRecentSource(cursor, hash):
        #sql = "SELECT sources_id, sources_date from sources WHERE sources_hash=%s AND sources_date < NOW() - INTERVAL %s day  LIMIT 1"
        sql = "SELECT sources_id, sources_date from sources WHERE sources_hash=%s AND sources_source IS NOT NULL LIMIT 1"

        #data = (hash, days)

        data = (hash,)

        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows



    def getResultsSource(cursor, hash):
        sql= "SELECT sources_source, sources_urls, sources_comments, sources_date from sources WHERE sources_hash=%s AND sources_source !='0'"
        data = (hash)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows


    def getAllResultsIdsByStudy(cursor, results_studies_id):
        sql= "SELECT * from results WHERE results_studies_id=%s"
        data = (results_studies_id)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows

    def countResultsbyStudy(cursor, studies_id):
        sql = "SELECT COUNT(results_id) FROM results, sources WHERE results_studies_id=%s AND results_hash = sources_hash"
        data = (studies_id)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows

    def countResultsbyStudySE(cursor, studies_id, se):
        sql = "SELECT COUNT(results_id) FROM results, sources WHERE results_studies_id=%s AND results_hash = sources_hash AND results_se =%s"
        data = (studies_id, se)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows


    def countClassifiedResultsbyStudy(cursor, studies_id):
        sql = "SELECT COUNT(DISTINCT classifications_id) FROM classifications, results WHERE classifications_hash = results_hash AND results_studies_id = %s"
        data = (studies_id)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows

    def countClassifiedResultsbyStudySE(cursor, studies_id, se):
        sql = "SELECT COUNT(DISTINCT classifications_id) FROM classifications, results WHERE classifications_hash = results_hash AND results_studies_id = %s AND results_se =%s"
        data = (studies_id, se)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows

    def countFailedResultsbyStudy(cursor, studies_id):
        sql = "SELECT COUNT(DISTINCT results_id) FROM sources, results WHERE sources_hash = results_hash AND results_studies_id = %s AND sources_source = '-1'"
        data = (studies_id)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows

    def countResultsQuery(cursor, results_queries_id):
        sql = "SELECT COUNT(results_id) FROM results WHERE results_queries_id = %s"
        data = (results_queries_id)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows

    def countClassifiedResultsbyQuery(cursor, results_queries_id):
        sql = "SELECT COUNT(DISTINCT classifications_id) FROM classifications, results WHERE classifications_hash = results_hash AND results_queries_id = %s"
        data = (results_queries_id)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows


    def getResultsIdsByStudyContact(cursor, results_studies_id, results_contact):
        sql= "SELECT * from results WHERE results_studies_id=%s AND results_contact=%s LIMIT 500"
        data = (results_studies_id, results_contact)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows

    def getResultById(cursor, results_id):
        sql= "SELECT results_id, results_hash from results WHERE results_id=%s"
        data = (results_id)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows

    def getResultByHash(cursor, hash):
        sql= "SELECT results_main, results_main_hash from results WHERE results_hash=%s"
        cursor.execute(sql,hash)
        rows = cursor.fetchall()
        return rows

    def getRecentResultByHash(cursor, hash):
        sql= "SELECT * from results WHERE results_hash=%s ORDER BY results_date DESC LIMIT 1"
        data = (hash)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows



    def insertEvaluationResult(cursor, evaluations_results_id, evaluations_module, evaluations_result):
        cursor.execute("INSERT INTO evaluations VALUES(%s,%s,%s) ON CONFLICT DO NOTHING;", (evaluations_results_id, evaluations_module, evaluations_result,))

    def getResultsSourcesNULL(cursor):
        sql= "SELECT results_hash, results_main_hash, results_url, results_main, results_id  FROM results   TABLESAMPLE SYSTEM_ROWS(50000)  LEFT JOIN sources ON results_hash = sources_hash WHERE sources_source is NULL"
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows



    def insertContactResult(cursor, contact_url, contact_hash, results_id):
        cursor.execute(
            "update results SET results_contact= %s, results_contact_hash = %s where results_id = %s",
            (contact_url, contact_hash, results_id)
        )


    def updateContactProgress(cursor, results_contact, results_id):
        cursor.execute(
            "update results SET results_contact= %s where results_id = %s",
            (results_contact, results_id)
        )



    def getResults(cursor):
        sql= "select results_id, results_position, results_queries_id, results_url, results_main, results_hash from results"
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows



    def getSourcesSpeedNULL(cursor):
        sql = "select distinct ON(sources_hash) sources_hash, results_url from sources, results TABLESAMPLE SYSTEM_ROWS(2000) where results_hash = sources_hash and sources_source IS NOT NULL and sources_source !='0' and sources_speed IS NULL"
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows


    def getResultHashesOnMain(cursor, main_hash):
        sql = "select distinct on(results_hash) results_hash from sources, results where results_hash = sources_hash and results_main_hash = %s  and sources_source IS NOT NULL and sources_source !='0'"
        cursor.execute(sql, (main_hash,))
        rows = cursor.fetchall()
        return rows

    def getSERP(cursor, query_id):
        sql= "SELECT serps_queries_id from serps WHERE serps_queries_id=%s"
        cursor.execute(sql,(query_id,))
        rows = cursor.fetchall()
        return rows

    def insertSERP(cursor, query_id, serp, serp_scraper, today):
        cursor.execute("INSERT INTO serps (serps_queries_id, serps_result, serps_scrapers_result, serps_date) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;", (query_id, serp, serp_scraper, today,))

    def deleteResults(cursor, queries_id, results_se):

        sql= "DELETE FROM sources USING results WHERE results_hash = sources_hash AND results_queries_id = %s AND results_se =%s"
        data = (queries_id, results_se)
        cursor.execute(sql,(data))

        sql= "DELETE FROM classifications USING results WHERE results_hash = classifications_hash AND results_queries_id = %s AND results_se =%s"
        data = (queries_id, results_se)
        cursor.execute(sql,(data))

        sql= "DELETE FROM evaluations USING results WHERE results_hash = evaluations_results_hash AND results_queries_id = %s AND results_se =%s"
        data = (queries_id, results_se)
        cursor.execute(sql,(data))

        sql= "DELETE FROM serps WHERE serps_queries_id = %s AND serps_se =%s"
        data = (queries_id, results_se)
        cursor.execute(sql,(data))

        sql= "DELETE from results WHERE results_queries_id=%s AND results_se =%s"
        data = (queries_id, results_se)
        cursor.execute(sql,(data))

        sql="DELETE FROM scrapers WHERE scrapers_queries_id	=%s AND scrapers_se=%s"
        data = (queries_id, results_se)
        cursor.execute(sql,(data))

    def deleteResultsNoScrapers(cursor, queries_id, results_se):
        sql= "DELETE FROM sources USING results WHERE results_hash = sources_hash AND results_queries_id = %s AND results_se =%s"
        data = (queries_id, results_se)
        cursor.execute(sql,(data))

        sql= "DELETE FROM classifications USING results WHERE results_hash = classifications_hash AND results_queries_id = %s AND results_se =%s"
        data = (queries_id, results_se)
        cursor.execute(sql,(data))

        sql= "DELETE FROM evaluations USING results WHERE results_hash = evaluations_results_hash AND results_queries_id = %s AND results_se =%s"
        data = (queries_id, results_se)
        cursor.execute(sql,(data))

        sql= "DELETE FROM serps WHERE serps_queries_id = %s AND serps_se =%s"
        data = (queries_id, results_se)
        cursor.execute(sql,(data))

        sql= "DELETE from results WHERE results_queries_id=%s AND results_se =%s"
        data = (queries_id, results_se)
        cursor.execute(sql,(data))
