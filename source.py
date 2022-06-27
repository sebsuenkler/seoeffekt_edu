from lib.sources import save_source

import sqlite3 as sl

connection = sl.connect('seo_effect.db')

cursor=connection.cursor()

urls = []

with connection:
    data = cursor.execute("SELECT SOURCE.id, SOURCE.result_id, SEARCH_RESULT.url FROM SOURCE,SEARCH_RESULT WHERE SOURCE.result_id = SEARCH_RESULT.id AND SOURCE.PROGRESS=? ORDER BY RANDOM() LIMIT 1", (0,))
    for row in data:
        source_id = row[0]
        result_id = row[1]
        url = row[2]

        urls.append([source_id, url])

for v in urls:
    source_id = v[0]

    with connection:
        cursor.execute("UPDATE SOURCE SET progress =? WHERE id =?", (2,source_id,))
        connection.commit()

for v in urls:
    source_id = v[0]
    url = v[1]
    source = save_source(url)

    with connection:
        cursor.execute("UPDATE SOURCE SET progress =?, source=? WHERE id =?", (1,source,source_id,))
        connection.commit()
