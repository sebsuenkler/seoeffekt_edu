import pandas as pd
import time
from db import *

connection = connect_to_db()
search_results = pd.read_sql_query("SELECT STUDY.id AS study_id, STUDY.name, QUERY.id AS query_id, QUERY.query, SEARCH_RESULT.id AS search_result_id, SEARCH_RESULT.search_engine, SEARCH_RESULT.position, SEARCH_RESULT.url FROM STUDY, SEARCH_RESULT, QUERY WHERE STUDY.id = SEARCH_RESULT.study_id AND QUERY.id = SEARCH_RESULT.query_id ORDER BY SEARCH_RESULT.id, SEARCH_RESULT.search_engine, SEARCH_RESULT.query_id, SEARCH_RESULT.position", connection)
close_connection_to_db(connection)


time.sleep(5)

connection = connect_to_db()
classified_results = pd.read_sql_query("SELECT STUDY.id AS study_id, STUDY.name, QUERY.id AS query_id, SEARCH_RESULT.id AS search_result_id, SEARCH_RESULT.search_engine, SEARCH_RESULT.position, SEARCH_RESULT.url, CLASSIFICATION.classification, CLASSIFICATION.value FROM STUDY, SEARCH_RESULT, QUERY, CLASSIFICATION WHERE STUDY.id = SEARCH_RESULT.study_id AND QUERY.id = SEARCH_RESULT.query_id AND SEARCH_RESULT.id = CLASSIFICATION.result_id ORDER BY SEARCH_RESULT.id, SEARCH_RESULT.search_engine, SEARCH_RESULT.query_id, SEARCH_RESULT.position", connection)
close_connection_to_db(connection)


if len(search_results) > len(classified_results):
    print("Tool is not finished with all tasks")

else:
    print("Tool is finished with all tasks")
