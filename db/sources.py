#Class for sources table

class Sources:

    def __init__(self, cursor):
        self.cursor = cursor


#read from db


#check existing pagespeed of stored sources
    def getSpeed(cursor, hash):
        sql= "SELECT sources_speed from sources WHERE sources_hash=%s LIMIT 1"
        data = (hash,)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows

    def getSourcesURLs(cursor, hash):
        sql= "SELECT sources_urls from sources WHERE sources_hash=%s LIMIT 1"
        data = (hash,)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows

    def resetSources(cursor):
        cursor.execute(
            "UPDATE sources SET sources_source = NULL, sources_speed = NULL WHERE sources_source = '-1' or sources_source = '1'"
        )


    def deleteSources(cursors, queries_id):
        pass
