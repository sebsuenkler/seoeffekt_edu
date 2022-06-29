import sqlite3 as sl

con = sl.connect('../seo_effect.db')

try:
    with con:
        con.execute("""
            CREATE TABLE study (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                date DATE
            );
        """)
except:
    pass

try:
    with con:
        con.execute("""
            CREATE TABLE source (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                result_id INTERGER,
                scraper_id INTEGER,
                source TEXT,
                progress INTEGER,
                date DATE
            );
        """)
except:
    pass


try:
    with con:
        con.execute("""
            CREATE TABLE scraper (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                study_id INTEGER,
                query_id INTEGER,
                query TEXT,
                search_engine TEXT,
                progress INTEGER,
                date DATE
            );
        """)
except:
    pass

try:
    with con:
        con.execute("""
            CREATE TABLE search_result (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                study_id INTEGER,
                query_id INTEGER,
                scraper_id INTEGER,
                ip TEXT,
                search_engine TEXT,
                position INTEGER,
                url TEXT,
                main_url TEXT,
                timestamp TIMESTAMP,
                date DATE
            );
        """)
except:
    pass


try:
    with con:
        con.execute("""
            CREATE TABLE query (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                study_id INTEGER,
                query TEXT,
                date DATE
            );
        """)
except:
    pass

try:
    with con:
        con.execute("""
            CREATE TABLE evaluation (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                result_id INTEGER,
                module TEXT,
                value TEXT,
                date DATE
            );
        """)
except:
    pass

try:
    with con:
        con.execute("""
            CREATE TABLE classification (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                result_id INTEGER,
                classification TEXT,
                value TEXT,
                date DATE
            );
        """)
except:
    pass
