import sqlite3 as sl

def connect_to_db():
    connection = sl.connect('seo_effect.db', timeout=10, isolation_level=None)
    connection.execute('pragma journal_mode=wal')
    return connection

def close_connection_to_db(connection):
    connection.close()
