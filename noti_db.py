import os
import psycopg2


def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)

conn = get_connection()
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS noti")
cur.execute("DROP TABLE IF EXISTS goods")
cur.execute("DROP TABLE IF EXISTS user_info")
cur.execute("DROP TABLE IF EXISTS templete")
cur.execute(
    "CREATE TABLE IF NOT EXISTS noti (number integer, name text, now integer, user_id text)")
cur.execute(
    "CREATE TABLE IF NOT EXISTS goods (name text, target text, capacity integer, stock integer, url text)")
cur.execute(
    "CREATE TABLE IF NOT EXISTS user_info (user_id text,reply_token text)")
cur.execute(
    "CREATE TABLE IF NOT EXISTS templete (name text, target text, capacity integer, stock integer, url text)")
cur.execute("INSERT INTO templete VALUES ('ティッシュ','人',1,1,'https://1.bp.blogspot.com/-dncnFat-Kf8/UV1JSxgmdaI/AAAAAAAAPXo/0aloQ-RKvEE/s1600/tissue.png')")
cur.execute("INSERT INTO templete VALUES ('ハンドソープ','人',1,1,'https://japaclip.com/files/hand-soap.png')")
cur.execute("INSERT INTO templete VALUES ('その他')")
cur.execute("INSERT INTO goods VALUES ('ティッシュ','人',100,20,'https://1.bp.blogspot.com/-dncnFat-Kf8/UV1JSxgmdaI/AAAAAAAAPXo/0aloQ-RKvEE/s1600/tissue.png')")
cur.execute("INSERT INTO goods VALUES ('ハンドソープ','人',30,1,'https://japaclip.com/files/hand-soap.png')")
cur.execute("INSERT INTO goods VALUES ('post','物',1,1,'https://japaclip.com/files/hand-soap.png')")
conn.commit()

def end():
    cur.close()
    conn.close()

def templeteList():
    cur.execute("SELECT * FROM templete")
    templeteList = cur.fetchall()
    print(templeteList)
    return templeteList

def register_id(user_id,reply_token):
    cur.execute(f"INSERT INTO user_info VALUES ('{user_id}','{reply_token}')")
    conn.commit()
    cur.execute("SELECT * FROM user_info")
    registerList = cur.fetchall()
    print(registerList)

def goodsList():
    cur.execute("SELECT * FROM goods")
    goodsList = cur.fetchall()
    print(goodsList)
    return goodsList
