#sys libs
import os, sys
import os.path

#tool libs
sys.path.insert(0, '..')
from db.connect import DB

sys.path.insert(0, '..')
from db.queries import Queries as DB_Queries

from libs.helpers import Helpers

# class for queries functions; mainly to read and write database content
class Queries:
    def __init__(self):
        self.data = []

#read from db

    def getQueriesStudy(study_id):
        db = DB()
        rows = DB_Queries.getQueriesStudy(db.cursor, study_id)
        db.DBDisconnect()
        return rows

    def getQueriesIdStudy(study_id):
        db = DB()
        rows = DB_Queries.getQueriesIdStudy(db.cursor, study_id)
        db.DBDisconnect()
        return rows

    def countQueriesStudy(studies_id):
        db = DB()
        rows = DB_Queries.countQueriesStudy(db.cursor, studies_id)
        db.DBDisconnect()
        return rows

#function to read all queries of a study
    def getQueriesNoScrapers(study_id):
        db = DB()
        rows = DB_Queries.getQueriesNoScrapers(db.cursor, study_id)
        db.DBDisconnect()
        return rows

#function to read all unprocessed queries
    def getOpenQueriesStudy(study_id):
        db = DB()
        rows = DB_Queries.getOpenQueriesStudy(db.cursor, study_id)
        db.DBDisconnect()
        return rows

    def getOpenQueriesStudybySE(study_id, se):
        db = DB()
        rows = DB_Queries.getOpenQueriesStudybySE(db.cursor, study_id, se)
        db.DBDisconnect()
        return rows

    def getOpenErrrorQueriesStudy(study_id):
        db = DB()
        rows = DB_Queries.getOpenErrrorQueriesStudy(db.cursor, study_id)
        db.DBDisconnect()
        return rows

#open one specific query
    def getQuery(study_id, query):
        db = DB()
        rows = DB_Queries.getQuery(db.cursor, study_id, query)
        db.DBDisconnect()
        return rows

    def getQuerybyID(query_id):
        db = DB()
        rows = DB_Queries.getQuerybyID(db.cursor, query_id)
        db.DBDisconnect()
        return rows

#open query of a result
    def getQuerybyResult(results_id):
        db = DB()
        rows = DB_Queries.getQuerybyResult(db.cursor, results_id)
        db.DBDisconnect()
        return rows

    def deleteQuery(studies_id, query):
        db = DB()
        rows = DB_Queries.deleteQuery(db.cursor, studies_id, query)
        db.DBDisconnect()


    def deleteQuerybyId(studies_id, queries_id):
        db = DB()
        rows = DB_Queries.deleteQuerybyId(db.cursor, studies_id, queries_id)
        db.DBDisconnect()

#write to db

#function to write query to db
    def insertQuery(study_id, query, date):
        db = DB()
        DB_Queries.insertQuery(db.cursor, study_id, query, date)
        db.DBDisconnect()

#function to write query to db with aditional information
    def insertQueryVal(study_id, query, comment, date):
        db = DB()
        DB_Queries.insertQueryVal(db.cursor, study_id, query, comment, date)
        db.DBDisconnect()
