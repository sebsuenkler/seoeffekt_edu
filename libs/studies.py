#sys libs
import os, sys
import os.path

#tool libs
sys.path.insert(0, '..')
from db.connect import DB

sys.path.insert(0, '..')
from db.studies import Studies as DB_Studies

from libs.helpers import Helpers

class Studies:
    def __init__(self):
        self.data = []

    def getStudies():
        db = DB()
        rows = DB_Studies.getStudies(db.cursor)
        db.DBDisconnect()
        return rows

    def getStudiesScraper():
        db = DB()
        rows = DB_Studies.getStudiesScraper(db.cursor)
        db.DBDisconnect()
        return rows

    def getStudy(study_id):
        db = DB()
        rows = DB_Studies.getStudy(db.cursor, study_id)
        db.DBDisconnect()
        return rows

    def getStudybyName(study_name):
        db = DB()
        rows = DB_Studies.getStudybyName(db.cursor, study_name)
        db.DBDisconnect()
        return rows

    def getStudybyNamenotID(study_name, study_id):
        db = DB()
        rows = DB_Studies.getStudybyNamenotID(db.cursor, study_name, study_id)
        db.DBDisconnect()
        return rows

    def insertStudy(study_name, study_description, today, study_se):
        db = DB()
        DB_Studies.insertStudy(db.cursor, study_name, study_description, today, study_se)
        db.DBDisconnect()

    def updateStudy(studies_name, studies_comment, studies_se, studies_id):
        db = DB()
        DB_Studies.updateStudy(db.cursor, studies_name, studies_comment, studies_se, studies_id)
        db.DBDisconnect()

    def deleteStudy(study_id):
        db = DB()
        DB_Studies.deleteStudy(db.cursor, study_id)
        db.DBDisconnect()

    def deleteunassignedResults():
        db = DB()
        DB_Studies.deleteunassignedResults(db.cursor)
        db.DBDisconnect()
