import sqlite3

dbpath = 'noti.db'
# データベース接続とカーソル生成
connection = sqlite3.connect(dbpath, check_same_thread=False)
# 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
# connection.isolation_level = None
cursor = connection.cursor()

def initialization():
    # エラー処理（例外処理）
    try:
        # CREATE
        # cursor.execute("DROP TABLE IF EXISTS noti")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS noti (number integer, name text, now integer)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS goods (name text, capacity integer, stock integer)")
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
    connection.commit()

def list():
    cursor.execute("SELECT * FROM goods")
    goodList = cursor.fetchall()
    return goodList

def add_noti(name):
    cursor.execute("SELECT * FROM noti")
    notiList = cursor.fetchall()
    count = len(notiList) + 1
    a = f"INSERT INTO goods VALUES ('{count}', {name}, 0)"
    # print(a)
    cursor.execute(a)
    connection.commit()

def add_goods(name,capacity,stock):
    a = f"INSERT INTO goods VALUES ('{name}', {capacity}, {stock})"
    # print(a)
    cursor.execute(a)
    connection.commit()

def end():
    # 保存を実行（忘れると保存されないので注意）
    connection.commit()
    # 接続を閉じる
    connection.close()
