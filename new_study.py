import csv
from datetime import date

import sqlite3 as sl

today = date.today()

print ("Form to insert a new study")

print("\n")

name = input("Insert the name of your study (required): ")

print("\n")

description = input("Insert description of your study (optional): ")

print("\n")

queries = input("Enter the filepath to your queries file: ")

print("\n")

# with open(queries) as csv_file:
#     csv_reader = csv.reader(csv_file)
#
#
# #    for row in csv_reader:
# #        print(row)

if not queries:
    queries = "test_queries.csv"

connection = sl.connect('seo_effect.db')

cursor=connection.cursor()

dup_name = False

search_engines = "Google.com_Top20"

with connection:
    data = cursor.execute("SELECT name FROM STUDY WHERE name =?", (name,))
    for row in data:
        dup_name = row

if not dup_name:
    sql = 'INSERT INTO STUDY(name, description, search_engines, date) values(?,?,?,?)'
    data = (name, description, "", today)

    with connection:
        cursor.execute(sql, data)
        study_id = cursor.lastrowid

    with open(queries) as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            dup_query = False
            query = row[0]
            data = cursor.execute("SELECT query FROM query WHERE query =?", (query,))
            for row in data:
                dup_query = row

            if not dup_query:
                sql = 'INSERT INTO query(study_id, query, date) values(?,?,?)'
                data = (study_id, query, today)

                with connection:
                    cursor.execute(sql, data)
            else:
                print("Query already exists (skip)")

else:
    print("Study already exists")
