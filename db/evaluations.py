#class for evaluations table

class Evaluations:
    def __init__(self, cursor):
        self.cursor = cursor


#read from db


#check existing module entries in the evaluations table
    def getEvaluationModule(cursor, hash, evaluations_module):
        sql= "SELECT evaluations_module from evaluations WHERE evaluations_results_hash=%s AND evaluations_module=%s LIMIT 1"
        data = (hash, evaluations_module)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows

    def getEvaluationModuleResult(cursor, hash, evaluations_module, evaluations_result):
        #sql= "SELECT evaluations_module from evaluations WHERE evaluations_results_hash=%s AND evaluations_module=%s AND evaluations_result=%s AND evaluations_date < NOW() - INTERVAL %s day LIMIT 1"
        sql= "SELECT evaluations_module from evaluations WHERE evaluations_results_hash=%s AND evaluations_module=%s AND evaluations_result=%s LIMIT 1"
        #data = (hash, evaluations_module, evaluations_result, days)
        data = (hash, evaluations_module, evaluations_result)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows

    def getResultHashes(cursor):
        sql = "SELECT distinct(results_hash) FROM results  TABLESAMPLE SYSTEM_ROWS(100000) JOIN sources ON results_hash = sources_hash LEFT JOIN evaluations ON results_hash = evaluations_results_hash WHERE sources_source IS NOT NULL and sources_source != '-1'"
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows

#read hashes with less than 53 evaluation results to select the unprocessed results and to check for missing values
    def getResultHashesNoUpdate(cursor, indicators):
        sql = "SELECT results_hash FROM results  TABLESAMPLE SYSTEM_ROWS(2000) JOIN sources ON results_hash = sources_hash LEFT JOIN evaluations ON results_hash = evaluations_results_hash WHERE sources_source IS NOT NULL and sources_source != '-1' GROUP BY 1 HAVING COUNT(evaluations_module) < %s"
        data = (indicators)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows

    def getResultwithIndicators(cursor, hash):
        sql = "SELECT distinct(results_hash), evaluations.*  FROM results, evaluations, sources WHERE results_hash = evaluations_results_hash AND sources_hash = evaluations_results_hash AND results_hash = %s AND sources_speed IS NOT NULL"
        data = (hash)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows

#read hashes with indicators and pagespeed
    def getResultstoClassify(cursor, indicators):

        #sql = "SELECT results_hash, results_url, results_main, sources_speed FROM results left join classifications on results_hash = classifications_hash JOIN sources ON sources_hash = results_hash JOIN evaluations ON results_hash = evaluations_results_hash WHERE classifications_hash IS NULL AND sources_speed IS NOT NULL GROUP BY 1,2,3,4 HAVING COUNT(evaluations_module) >= %s"

        sql = "SELECT results_hash, results_url, results_main, sources_speed FROM results left join classifications on results_hash = classifications_hash JOIN sources ON sources_hash = results_hash JOIN evaluations ON results_hash = evaluations_results_hash WHERE classifications_hash IS NULL AND sources_speed IS NOT NULL GROUP BY 1,2,3,4 HAVING COUNT(DISTINCT(evaluations_module)) >= %s"
        data = (indicators)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows

    def getResultstoClassifyCheck(cursor):

        sql="select classifications_hash, string_agg(classifications_classification, ',') FROM classifications WHERE classifications_result != 'unassigned' GROUP BY 1 HAVING COUNT(classifications_classification) = 1 ORDER BY RANDOM() LIMIT 200"
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows

    def getResultstoUpdateClassification(cursor, classifier_id, classifier_result):

        #sql = "SELECT results_hash, results_url, results_main, sources_speed FROM results left join classifications on results_hash = classifications_hash JOIN sources ON sources_hash = results_hash JOIN evaluations ON results_hash = evaluations_results_hash WHERE classifications_hash IS NULL AND sources_speed IS NOT NULL GROUP BY 1,2,3,4 HAVING COUNT(evaluations_module) >= %s"

        sql = "SELECT classifications_hash, results_url, results_main, sources_speed FROM results join classifications on results_hash = classifications_hash JOIN sources ON sources_hash = results_hash WHERE classifications_classification = %s AND classifications_result = %s GROUP BY 1,2,3,4"
        data = (classifier_id, classifier_result)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows

    def getUnassigned(cursor):

        sql = "SELECT classifications_id FROM classifications WHERE classifications_result = 'unassigned' LIMIT 1"
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows


    def getEvaluationsResults(cursor, hash):
        sql = "SELECT evaluations_module, evaluations_result FROM evaluations WHERE evaluations_results_hash = %s"
        data = (hash)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows

    def getEvaluationModules(cursor):
        sql = "SELECT DISTINCT(evaluations_module) FROM evaluations"
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows


#write to db


#insert indicators, results of url categories and plugins evaluations to the table
    def insertEvaluationResult(cursor, evaluations_results_hash, evaluations_module, evaluations_result, evaluations_date):
        cursor.execute("INSERT INTO evaluations VALUES(%s,%s,%s, %s) ON CONFLICT DO NOTHING;", (evaluations_results_hash, evaluations_module, evaluations_result, evaluations_date,))

#update evaulation results
    def UpdateEvaluationResult(cursor, value, date, hash, module):
        cursor.execute(
            "UPDATE evaluations SET evaluations_result= %s, evaluations_date = %s WHERE evaluations_results_hash = %s and evaluations_module = %s",
            (value, date, hash, module)
        )

    def insertClassificationResult(cursor, hash, result, classifications_classification, today):
        cursor.execute("INSERT INTO classifications (classifications_hash, classifications_result, classifications_classification, classifications_date) VALUES(%s,%s,%s,%s) ON CONFLICT DO NOTHING;", (hash, result, classifications_classification, today,))


    def updateClassificationResult(cursor, hash, result, classifications_classification, today):
        cursor.execute(
            "UPDATE classifications SET classifications_result= %s, classifications_date = %s WHERE classifications_hash = %s and classifications_classification = %s",
            (result, today, hash, classifications_classification)
        )

    def getClassificationResult(cursor, hash, classifications_classification):
        sql = "SELECT classifications_result FROM classifications WHERE classifications_hash = %s AND classifications_classification = %s LIMIT 1"
        data = (hash, classifications_classification)
        cursor.execute(sql,data)
        rows = cursor.fetchall()
        return rows

    def getClassificationResultValue(cursor, hash, classifications_classification, classifier_result):
        sql = "SELECT classifications_result FROM classifications WHERE classifications_hash = %s AND classifications_classification = %s AND classifications_result = %s LIMIT 1"
        data = (hash, classifications_classification, classifier_result)
        cursor.execute(sql,data)
        rows = cursor.fetchall()
        return rows

#delete from db

#remove duplicates
    def deleteDuplicates(cursor):
        sql = "DELETE FROM evaluations WHERE evaluations_id IN (SELECT evaluations_id FROM(SELECT evaluations_id,ROW_NUMBER() OVER( PARTITION BY evaluations_results_hash,evaluations_module ORDER BY evaluations_id) AS row_num FROM evaluations) t WHERE t.row_num > 1 );"
        cursor.execute(sql)


    def deleteDupClassifiedData(cursor):
        sql = "DELETE FROM classifications WHERE classifications_id IN (SELECT classifications_id FROM(SELECT classifications_id,ROW_NUMBER() OVER( PARTITION BY classifications_hash,classifications_classification ORDER BY classifications_id) AS row_num FROM classifications) t WHERE t.row_num > 1 )"
        cursor.execute(sql)

    def getEvaluationsDate(cursor, hash, module):
        sql= "SELECT evaluations_date from evaluations WHERE evaluations_results_hash=%s AND evaluations_module=%s LIMIT 1"
        data = (hash, module)
        cursor.execute(sql,data)
        rows = cursor.fetchall()
        return rows


    def deleteEvaluations(cursor, queries_id):
        pass

    def deleteClassifications(cursor, queries_id):
        pass
