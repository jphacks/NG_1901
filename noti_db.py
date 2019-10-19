import os
import psycopg2


def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)

conn = get_connection()
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS user_info")
cur.execute(
    "CREATE TABLE IF NOT EXISTS noti (number integer, name text, now integer, user_id text)")
cur.execute(
    "CREATE TABLE IF NOT EXISTS goods (name text, capacity integer, stock integer, url text)")
cur.execute(
    "CREATE TABLE IF NOT EXISTS templete (name text, capacity integer, stock integer, url text)")
cur.execute("INSERT INTO templete VALUES ('ティッシュ')")
cur.execute("INSERT INTO templete VALUES ('ハンドソープ')")
cur.execute("INSERT INTO templete VALUES ('その他')")
conn.commit()

def end():
    cur.close()
    conn.close()

def templeteList():
    cur.execute("SELECT * FROM templete")
    templeteList = cur.fetchall()
    print(templeteList)
    return templeteList
