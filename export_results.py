import pandas as pd

from db import *

file_name = False
while not file_name:
    file_name = input("Insert the filename without file exentions to export results to CSV (required): ")

connection = connect_to_db()
search_results = pd.read_sql_query("SELECT STUDY.id AS study_id, STUDY.name, QUERY.id AS query_id, QUERY.query, SEARCH_RESULT.id AS search_result_id, SEARCH_RESULT.search_engine, SEARCH_RESULT.position, SEARCH_RESULT.url FROM STUDY, SEARCH_RESULT, QUERY WHERE STUDY.id = SEARCH_RESULT.study_id AND QUERY.id = SEARCH_RESULT.query_id ORDER BY SEARCH_RESULT.id, SEARCH_RESULT.search_engine, SEARCH_RESULT.query_id, SEARCH_RESULT.position", connection)
close_connection_to_db(connection)

# Verify that result of SQL query is stored in the dataframe

file_name_search_results = file_name+"_search_results.csv"

search_results.to_csv(file_name_search_results, sep='\t')


connection = connect_to_db()
classified_results = pd.read_sql_query("SELECT STUDY.id AS study_id, STUDY.name, QUERY.id AS query_id, SEARCH_RESULT.id AS search_result_id, SEARCH_RESULT.search_engine, SEARCH_RESULT.position, SEARCH_RESULT.url, CLASSIFICATION.classification, CLASSIFICATION.value FROM STUDY, SEARCH_RESULT, QUERY, CLASSIFICATION WHERE STUDY.id = SEARCH_RESULT.study_id AND QUERY.id = SEARCH_RESULT.query_id AND SEARCH_RESULT.id = CLASSIFICATION.result_id ORDER BY SEARCH_RESULT.id, SEARCH_RESULT.search_engine, SEARCH_RESULT.query_id, SEARCH_RESULT.position", connection)
close_connection_to_db(connection)

# Verify that result of SQL query is stored in the dataframe

if len(search_results) > len(classified_results):
    proceed = "x"
    while proceed != "y" and proceed !="n":
        proceed = input("The classification is not done, do you want to download the partial results (y/n)?: ")
        proceed = proceed.lower()

    if proceed == "y":

        file_name_classified_results = file_name+"_partial_classified_results.csv"

        classified_results.to_csv(file_name_classified_results, sep='\t')

        connection = connect_to_db()
        indicators_results = pd.read_sql_query("SELECT STUDY.id AS study_id, STUDY.name, QUERY.id AS query_id, SEARCH_RESULT.id AS search_result_id, SEARCH_RESULT.search_engine, SEARCH_RESULT.position, SEARCH_RESULT.url, CLASSIFICATION.classification, CLASSIFICATION.value, EVALUATION.module, EVALUATION.value FROM STUDY, SEARCH_RESULT, QUERY, CLASSIFICATION, EVALUATION WHERE STUDY.id = SEARCH_RESULT.study_id AND QUERY.id = SEARCH_RESULT.query_id AND SEARCH_RESULT.id = CLASSIFICATION.result_id AND SEARCH_RESULT.id = EVALUATION.result_id ORDER BY SEARCH_RESULT.id, SEARCH_RESULT.search_engine, SEARCH_RESULT.query_id, SEARCH_RESULT.position", connection)
        close_connection_to_db(connection)

        file_name_indicators_results = file_name+"_partial_indcators_results.csv"

        indicators_results.to_csv(file_name_indicators_results, sep='\t')

    else:
        exit()

else:

        file_name_classified_results = file_name+"_classified_results.csv"

        classified_results.to_csv(file_name_classified_results, sep='\t')

        connection = connect_to_db()
        indicators_results = pd.read_sql_query("SELECT STUDY.id AS study_id, STUDY.name, QUERY.id AS query_id, SEARCH_RESULT.id AS search_result_id, SEARCH_RESULT.search_engine, SEARCH_RESULT.position, SEARCH_RESULT.url, CLASSIFICATION.classification, CLASSIFICATION.value, EVALUATION.module, EVALUATION.value FROM STUDY, SEARCH_RESULT, QUERY, CLASSIFICATION, EVALUATION WHERE STUDY.id = SEARCH_RESULT.study_id AND QUERY.id = SEARCH_RESULT.query_id AND SEARCH_RESULT.id = CLASSIFICATION.result_id AND SEARCH_RESULT.id = EVALUATION.result_id ORDER BY SEARCH_RESULT.id, SEARCH_RESULT.search_engine, SEARCH_RESULT.query_id, SEARCH_RESULT.position", connection)
        close_connection_to_db(connection)

        file_name_indicators_results = file_name+"_indcators_results.csv"

        indicators_results.to_csv(file_name_indicators_results, sep='\t')
