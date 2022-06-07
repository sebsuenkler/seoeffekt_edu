#Class to connect to the Database

import psycopg2
import json
import os

config_path = '/home/alpha/config/'

with open(config_path+'db.ini', 'r') as f:
    array = json.load(f)

dbname = array['dbname']
user = array['user']
host = array['host']
password = array['password']


db_connection = ("dbname='"+dbname+"' user='"+user+"' host='"+host+"' " + \
                  "password='"+password+"' connect_timeout=3000")


class DB:
    def __init__(self, db_string = db_connection):
        self.__connection = psycopg2.connect(db_string)
        self.__connection.autocommit = True
        self.__cursor = self.__connection.cursor()

    def __getCursor(self):
        return self.__cursor


    def DBDisconnect(self):
        self.__cursor.close()
        self.__connection.close()

    cursor = property(__getCursor)
