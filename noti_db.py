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
    "CREATE TABLE IF NOT EXISTS noti (noti_name text, goods_name text, now integer, user_id text, reply_token text)")
cur.execute(
    "CREATE TABLE IF NOT EXISTS goods (goods_name text, target text, capacity integer, stock integer, url text)")
cur.execute(
    "CREATE TABLE IF NOT EXISTS user_info (user_id text,reply_token text)")
cur.execute(
    "CREATE TABLE IF NOT EXISTS templete (goods_name text, target text, capacity integer, stock integer, url text)")
cur.execute("INSERT INTO templete VALUES ('ティッシュ','人',1,1,'https://1.bp.blogspot.com/-dncnFat-Kf8/UV1JSxgmdaI/AAAAAAAAPXo/0aloQ-RKvEE/s1600/tissue.png')")
cur.execute("INSERT INTO templete VALUES ('ハンドソープ','人',1,1,'https://japaclip.com/files/hand-soap.png')")
cur.execute("INSERT INTO templete VALUES ('その他')")
cur.execute("INSERT INTO goods VALUES ('ティッシュ','人',100,20,'https://1.bp.blogspot.com/-dncnFat-Kf8/UV1JSxgmdaI/AAAAAAAAPXo/0aloQ-RKvEE/s1600/tissue.png')")
cur.execute("INSERT INTO goods VALUES ('ハンドソープ','人',30,1,'https://japaclip.com/files/hand-soap.png')")
cur.execute("INSERT INTO goods VALUES ('post','物',1,1,'https://japaclip.com/files/hand-soap.png')")
cur.execute("INSERT INTO noti VALUES ('noti1','ティッシュ',1,'aaaaa','xxxxxxx')")
cur.execute("INSERT INTO noti VALUES ('noti2','ハンドソープ',1,'aaaaa','xxxxxxx')")
conn.commit()

def end():
    cur.close()
    conn.close()

def templeteList():
    cur.execute("SELECT * FROM templete")
    templete_list = cur.fetchall()
    print(templete_list)
    return templete_list

def registerId(user_id,reply_token):
    cur.execute(f"INSERT INTO user_info VALUES ('{user_id}','{reply_token}')")
    conn.commit()
    cur.execute("SELECT * FROM user_info")
    register_list = cur.fetchall()
    print(register_list)

def goodsList():
    cur.execute("SELECT * FROM goods")
    goods_list = cur.fetchall()
    print(goods_list)
    return goods_list

def selectReplyToken(noti_name):
    cur.execute("SELECT reply_token FROM noti WHERE noti_name=%s",(f'{noti_name}',))
    reply_token = cur.fetchall()
    return reply_token[0][0]

def selectUserId(noti_name):
    cur.execute("SELECT user_id FROM noti WHERE noti_name=%s",(f'{noti_name}',))
    user_id = cur.fetchall()
    return user_id[0][0]
