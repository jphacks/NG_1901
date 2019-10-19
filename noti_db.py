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
    "CREATE TABLE IF NOT EXISTS user_info (user_id text,reply_token text)")
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

def register_id(user_id,reply_token):
    cur.execute(f"INSERT INTO user_info VALUES ('{user_id}','{reply_token}')")
    conn.commit()
    cur.execute("SELECT * FROM user_info")
    registerList = cur.fetchall()
    print(registerList)

# import sqlite3
#
# dbpath = 'noti.db'
# # データベース接続とカーソル生成
# connection = sqlite3.connect(dbpath, check_same_thread=False)
# # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
# # connection.isolation_level = None
# cursor = connection.cursor()
#
# def initialization():
#     # エラー処理（例外処理）
#     try:
#         # CREATE
#         # cursor.execute("DROP TABLE IF EXISTS noti")
#         # cursor.execute("DROP TABLE IF EXISTS goods")
#         cursor.execute(
#             "CREATE TABLE IF NOT EXISTS noti (number integer, name text, now integer, user_id text)")
#         cursor.execute(
#             "CREATE TABLE IF NOT EXISTS goods (name text, capacity integer, stock integer, url text)")
#         cursor.execute(
#             "CREATE TABLE IF NOT EXISTS user_info (user_id text, reply_token text)")
#         cursor.execute(
#             "CREATE TABLE IF NOT EXISTS templete (name text, capacity integer, stock integer, url text)")
#         cursor.execute("INSERT INTO templete VALUES ('ティッシュ', , )")
#         cursor.execute("INSERT INTO templete VALUES ('ハンドソープ', , )")
#         cursor.execute("INSERT INTO templete VALUES ('その他', , )")
#
#     except sqlite3.Error as e:
#         print('sqlite3.Error occurred:', e.args[0])
#     connection.commit()
#
# def list():
#     cursor.execute("SELECT * FROM noti")
#     goodList = cursor.fetchall()
#     print(goodList)
#     return goodList
#
# def add_noti(name):
#     cursor.execute("SELECT * FROM noti")
#     notiList = cursor.fetchall()
#     count = len(notiList) + 1
#     a = f"INSERT INTO goods VALUES ('{count}', {name}, 0)"
#     # print(a)
#     cursor.execute(a)
#     connection.commit()
#
# def add_goods(name,capacity,stock):
#     a = f"INSERT INTO goods VALUES ('{name}', {capacity}, {stock})"
#     # print(a)
#     cursor.execute(a)
#     connection.commit()
#
# def end():
#     # 保存を実行（忘れると保存されないので注意）
#     connection.commit()
#     # 接続を閉じる
#     connection.close()
