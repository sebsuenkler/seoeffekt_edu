import sqlite3 as sl

import datetime

def write_to_log(timestamp, content):
    f = open("main.log", "a+")
    f.write(timestamp+": "+content+"\n")
    f.close()


def connect_to_db():
    connection = sl.connect('seo_effect.db', timeout=10, isolation_level=None)
    connection.execute('pragma journal_mode=wal')
    return connection

def close_connection_to_db(connection):
    connection.close()




timestamp = datetime.datetime.now()
timestamp = timestamp.strftime("%d-%m-%Y, %H:%M:%S")

write_to_log(timestamp, "Stop the tool")


import psutil
for proc in psutil.process_iter(attrs=['pid', 'name']):
    if 'python' in proc.info['name']:

        if "main.py" in proc.cmdline():
            proc.kill()

        try:
            if "job_classifier.py" in proc.cmdline():
                proc.kill()
        except:
            pass

        try:
            if "job_reset_scraper.py" in proc.cmdline():
                proc.kill()
        except:
            pass

        try:
            if "job_scraper.py" in proc.cmdline():
                proc.kill()
        except:
            pass

        try:
            if "job_source.py" in proc.cmdline():
                proc.kill()
        except:
            pass

urls = []

connection = connect_to_db()
cursor = connection.cursor()
data = cursor.execute("SELECT SOURCE.id, SOURCE.result_id, SEARCH_RESULT.url FROM SOURCE,SEARCH_RESULT WHERE SOURCE.result_id = SEARCH_RESULT.id AND SOURCE.PROGRESS=? ", (2,))
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
    cursor.execute("UPDATE SOURCE SET progress =? WHERE id =?", (0,source_id,))
    connection.commit()
    close_connection_to_db(connection)


reset_ids = []

connection = connect_to_db()
cursor = connection.cursor()
data = cursor.execute("SELECT id FROM SCRAPER WHERE progress =?", (2,))
connection.commit()
for row in data:
    id = row[0]
    reset_ids.append(id)

close_connection_to_db(connection)

if reset_ids:
    for r_id in reset_ids:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("UPDATE SCRAPER SET progress =? WHERE id =?", (0,r_id,))
        connection.commit()
        close_connection_to_db(connection)

        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM SEARCH_RESULT WHERE scraper_id =?", (r_id,))
        connection.commit()
        close_connection_to_db(connection)

        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM SOURCE WHERE scraper_id =?", (r_id,))
        connection.commit()
        close_connection_to_db(connection)
