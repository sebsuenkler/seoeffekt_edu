#sys libs
import os, sys
import os.path

#tool libs
sys.path.insert(0, '..')
from db.connect import DB

sys.path.insert(0, '..')
from db.sources import Sources as DB_Sources

from libs.helpers import Helpers

# class for evaluatios functions; mainly to read and write database content; the library is necessary to process indicators
class Sources:
    def __init__(self):
        self.data = []

#helper to check for loading speed entries in the sources table
    def getSpeed(hash):
        db = DB()
        rows = DB_Sources.getSpeed(db.cursor, hash)
        db.DBDisconnect()
        return rows

    def getSourcesURLs(hash):
        db = DB()
        rows = DB_Sources.getSourcesURLs(db.cursor, hash)
        db.DBDisconnect()
        return rows

    def resetSources():
        db = DB()
        DB_Sources.resetSources(db.cursor)
        db.DBDisconnect()

    def deleteSources(query_id):
        pass
