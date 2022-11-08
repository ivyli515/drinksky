import os
import psycopg2
from contextlib2 import closing

DB_URL = os.environ.get('DATABASE_URL', 'dbname=drinksky')

def sql_select_all(query, parameters):
    with closing(psycopg2.connect('dbname = drinksky')) as conn, conn.cursor() as cur:
        cur.execute(query,parameters)
        result = cur.fetchall()
        return result

def sql_select_one(query, parameters):
    with closing(psycopg2.connect('dbname = drinksky')) as conn, conn.cursor() as cur:
        cur.execute(query,parameters)
        result = cur.fetchone()
        return result

def sql_write(query, parameters):
    with closing(psycopg2.connect('dbname = drinksky')) as conn, conn.cursor() as cur:
        cur.execute(query,parameters)
        conn.commit()