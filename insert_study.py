import csv
import json
from datetime import date

import sqlite3 as sl

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

origin_results = input("Do you want to scrape search results (y/n)?: ")

print("\n")
if origin_results == "y":
    while not search_engines:
        for search_engine in search_engines_json:
            se_choice = ""
            while se_choice.lower() != "y" or se_choice.lower() != "n":
                se_choice = input("Do you want to include {} (y/n)?: ".format(search_engine))
                if se_choice.lower() == "y":
                    search_engines.append(search_engine)
                    break;
                elif se_choice.lower() == "n":
                    break;
                else:
                    pass

print("\n")

import_results = input("Do you want to import results (y/n)?: ")

queries = input("Enter the filepath to your queries file (default: queries.csv): ")

print("\n")

if not queries:
    queries = "queries.csv"

connection = sl.connect('seo_effect.db')

cursor=connection.cursor()

dup_name = False

with connection:
    data = cursor.execute("SELECT name FROM STUDY WHERE name =?", (name,))
    for row in data:
        dup_name = row

if not dup_name:
    sql = 'INSERT INTO STUDY(name, description, date) values(?,?,?)'
    data = (name, description, today)

    with connection:
        cursor.execute(sql, data)
        study_id = cursor.lastrowid

    with open(queries) as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            dup_query = False
            query = row[0]
            data = cursor.execute("SELECT query FROM query WHERE query =? and study_id =?", (query,study_id,))
            for row in data:
                dup_query = row

            if not dup_query:
                sql = 'INSERT INTO query(study_id, query, date) values(?,?,?)'
                data = (study_id, query, today)

                with connection:
                    cursor.execute(sql, data)
                    query_id = cursor.lastrowid
                    progress = 0
                    for search_engine in search_engines:
                        sql = 'INSERT INTO scraper(study_id, query_id, query, search_engine, progress, date) values(?,?,?,?,?,?)'
                        data = (study_id, query_id, query, search_engine, progress, today)
                        cursor.execute(sql, data)

            else:
                print("Query already exists (skip)")



else:
    print("Study with the same name already exists")
