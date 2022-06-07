#Class for studies table
class Studies:
    def __init__(self, cursor):
        self.cursor = cursor

    def getStudies(cursor):
        cursor.execute("SELECT * from studies")
        rows = cursor.fetchall()
        return rows

    def getStudiesScraper(cursor):
        cursor.execute("SELECT * from studies WHERE import IS NULL")
        rows = cursor.fetchall()
        return rows

    def getStudy(cursor, id):
        sql= "SELECT * from studies WHERE studies_id=%s"
        data = (id)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows

    def getStudybyName(cursor, studies_name):
        sql= "SELECT studies_name, studies_comment, studies_date, studies_se, studies_id from studies WHERE studies_name=%s"
        data = (studies_name)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows

    def getStudybyNamenotID(cursor, studies_name, studies_id):
        sql= "SELECT studies_name from studies WHERE studies_name=%s AND studies_id != %s"
        data = (studies_name, studies_id)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows

    def updateStudy(cursor, studies_name, studies_comment, studies_se, studies_id):
        cursor.execute(
            "UPDATE studies SET studies_name= %s, studies_comment = %s, studies_se = %s WHERE studies_id = %s",
            (studies_name, studies_comment, studies_se, studies_id)
        )


    def insertStudy(cursor, studies_name, studies_comment, studies_date, studies_se):
        cursor.execute("INSERT INTO studies (studies_name, studies_comment, studies_date, studies_se) VALUES(%s,%s,%s,%s);", (studies_name, studies_comment, studies_date, studies_se))

    def deleteStudy(cursor, studies_id):
        #delete from studies
        sql= "DELETE from studies WHERE studies_id=%s"
        data = (studies_id)
        cursor.execute(sql,(data,))

        #delete from classifications
        sql = "DELETE from classifications USING results WHERE classifications_hash = results_hash AND results_studies_id = %s"
        data = (studies_id)
        cursor.execute(sql,(data,))

        #delete from scrapers
        sql = "DELETE from scrapers USING results WHERE scrapers_studies_id = results_studies_id AND results_studies_id = %s"
        data = (studies_id)
        cursor.execute(sql,(data,))

        #delete from sources
        sql = "DELETE from sources USING results WHERE sources_hash = results_hash AND results_studies_id = %s"
        data = (studies_id)
        cursor.execute(sql,(data,))

        #delete from serps
        sql = "DELETE from serps USING queries WHERE serps_queries_id = queries_id AND queries_studies_id = %s"
        data = (studies_id)
        cursor.execute(sql,(data,))

        #delete from evaluations
        sql = "DELETE from evaluations USING results WHERE evaluations_results_hash = results_hash AND results_studies_id = %s"
        data = (studies_id)
        cursor.execute(sql,(data,))

        #delete from queries
        sql = "DELETE from queries WHERE queries_studies_id = %s"
        data = (studies_id)
        cursor.execute(sql,(data,))

        #delete from results
        sql= "DELETE from results WHERE results_studies_id=%s"
        data = (studies_id)
        cursor.execute(sql,(data,))

    #function to delete deleteunassignedResults = results which are not related to a study
    def deleteunassignedResults(cursor):
        #delete from classifications
        sql = "DELETE from classifications USING results WHERE classifications_hash = results_hash AND NOT EXISTS(SELECT * FROM studies WHERE studies_id = results_studies_id)"
        cursor.execute(sql)

        #delete from scrapers
        sql = "DELETE from scrapers USING results WHERE scrapers_queries_id = results_queries_id AND NOT EXISTS(SELECT * FROM studies WHERE studies_id = results_studies_id)"
        cursor.execute(sql)

        #delete from sources
        sql = "DELETE from sources USING results WHERE sources_hash = results_hash AND NOT EXISTS(SELECT * FROM studies WHERE studies_id = results_studies_id)"
        cursor.execute(sql)

        #delete from serps
        sql = "DELETE from serps USING queries WHERE serps_queries_id = queries_id AND NOT EXISTS(SELECT * FROM studies WHERE studies_id = queries_studies_id)"
        cursor.execute(sql)

        #delete from evaluations
        sql = "DELETE from evaluations USING results WHERE evaluations_results_hash = results_hash AND NOT EXISTS(SELECT * FROM studies WHERE studies_id = results_studies_id)"
        cursor.execute(sql)

        #delete from queries
        sql = "DELETE from queries WHERE NOT EXISTS(SELECT * FROM studies WHERE studies_id = queries_studies_id)"

        #delete from results
        sql= "DELETE from results WHERE NOT EXISTS(SELECT * FROM studies WHERE studies_id = results_studies_id)"
        cursor.execute(sql)
