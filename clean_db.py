from db import *

connection = connect_to_db()
connection.execute('VACUUM;')

close_connection_to_db(connection)
