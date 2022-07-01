from lib.sources import save_source

import datetime

from db import *
from log import *

urls = []

connection = connect_to_db()
cursor = connection.cursor()
data = cursor.execute("SELECT SOURCE.id, SOURCE.result_id, SEARCH_RESULT.url FROM SOURCE,SEARCH_RESULT WHERE SOURCE.result_id = SEARCH_RESULT.id AND SOURCE.PROGRESS=? ORDER BY RANDOM() LIMIT 10", (0,))
connection.commit()

for row in data:
    source_id = row[0]
    result_id = row[1]
    url = row[2]

    urls.append([source_id, url])

close_connection_to_db(connection)

for v in urls:
    connection = connect_to_db()
    cursor = connection.cursor()
    source_id = v[0]
    cursor.execute("UPDATE SOURCE SET progress =? WHERE id =?", (2,source_id,))
    connection.commit()
    close_connection_to_db(connection)


for v in urls:
    connection = connect_to_db()
    cursor = connection.cursor()
    source_id = v[0]
    url = v[1]
    source = save_source(url)

    cursor.execute("UPDATE SOURCE SET progress =?, source=? WHERE id =?", (1,source,source_id,))
    connection.commit()
    close_connection_to_db(connection)

    timestamp = datetime.datetime.now()
    timestamp = timestamp.strftime("%d-%m-%Y, %H:%M:%S")

    write_to_log(timestamp, "Save Source "+str(url))
