# Import Search Queries

#include libs

import sys
sys.path.insert(0, '..')
from include import *

#select csv file with search queries
queries_file = "search_queries.csv"

#select study
study_id = 10

#open csv file with queries
with open(queries_file, 'r') as csvfile:
    queries = csv.reader(csvfile)

    #insert queries to database
    for query in queries:
        print(query[0])
        Queries.insertQuery(study_id, query[0])
