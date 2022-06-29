import csv
import json
from datetime import date

import sqlite3 as sl


def connect_to_db():
    connection = sl.connect('seo_effect.db', timeout=10, isolation_level=None)
    connection.execute('pragma journal_mode=wal')
    return connection

def close_connection_to_db(connection):
    connection.close()

today = date.today()

search_engines = []

with open('scraper.json') as json_file:
    search_engines_json = json.load(json_file)

print ("Form to insert a new study")

print("\n")

name = False
while not name:
    name = input("Insert the name of your study (required): ")

print("\n")

description = input("Insert description of your study (optional): ")

print("\n")

print("Select Search Engines:")

while not search_engines:
    for search_engine in search_engines_json:
        se_choice = ""
        while se_choice.lower() != "y" or se_choice.lower() != "n":
            se_choice = input("Do you want to scrape {} (y/n)?: ".format(search_engine))
            if se_choice.lower() == "y":
                search_engines.append(search_engine)
                break;
            elif se_choice.lower() == "n":
                break;
            else:
                pass

print("\n")


queries = input("Enter the filepath to your queries file (default: queries.csv): ")

print("\n")

if not queries:
    queries = "queries.csv"


dup_name = False

connection = connect_to_db()
cursor = connection.cursor()
data = cursor.execute("SELECT name FROM STUDY WHERE name =?", (name,))
connection.commit()
for row in data:
    dup_name = row
close_connection_to_db(connection)

if not dup_name:
    connection = connect_to_db()
    cursor = connection.cursor()
    sql = 'INSERT INTO STUDY(name, description, date) values(?,?,?)'
    data = (name, description, today)

    cursor.execute(sql, data)
    connection.commit()
    study_id = cursor.lastrowid
    close_connection_to_db(connection)

    with open(queries) as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            dup_query = False
            query = row[0]
            connection = connect_to_db()
            cursor = connection.cursor()
            data = cursor.execute("SELECT query FROM query WHERE query =? and study_id =?", (query,study_id,))
            connection.commit()
            for row in data:
                dup_query = row
            close_connection_to_db(connection)

            if not dup_query:
                connection = connect_to_db()
                cursor = connection.cursor()
                sql = 'INSERT INTO query(study_id, query, date) values(?,?,?)'
                data = (study_id, query, today)
                cursor.execute(sql, data)
                connection.commit()
                query_id = cursor.lastrowid
                progress = 0
                close_connection_to_db(connection)

                for search_engine in search_engines:
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    sql = 'INSERT INTO scraper(study_id, query_id, query, search_engine, progress, date) values(?,?,?,?,?,?)'
                    data = (study_id, query_id, query, search_engine, progress, today)
                    cursor.execute(sql, data)
                    connection.commit()
                    close_connection_to_db(connection)
            else:
                print("Query already exists (skip)")



else:
    print("Study with the same name already exists")
