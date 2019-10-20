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
    "CREATE TABLE IF NOT EXISTS noti (noti_name text, goods_name text, now integer, user_id text, capacity integer)")
cur.execute(
    "CREATE TABLE IF NOT EXISTS goods (goods_name text, target text, capacity integer, stock integer, url text)")
cur.execute(
    "CREATE TABLE IF NOT EXISTS user_info (user_id text,reply_token text)")
cur.execute(
    "CREATE TABLE IF NOT EXISTS templete (goods_name text, target text, capacity integer, stock integer, url text)")
cur.execute("INSERT INTO templete VALUES ('ティッシュ','人',1,1,'https://1.bp.blogspot.com/-dncnFat-Kf8/UV1JSxgmdaI/AAAAAAAAPXo/0aloQ-RKvEE/s1600/tissue.png')")
cur.execute("INSERT INTO templete VALUES ('ハンドソープ','人',1,1,'https://japaclip.com/files/hand-soap.png')")
cur.execute("INSERT INTO templete VALUES ('その他','人',1,1,'https://i1.wp.com/sozaikoujou.com/wordpress/wp-content/uploads/2016/06/th_app_button_plus.jpg?w=600&ssl=1')")
# cur.execute("INSERT INTO goods VALUES ('ティッシュ','人',3,1,'https://1.bp.blogspot.com/-dncnFat-Kf8/UV1JSxgmdaI/AAAAAAAAPXo/0aloQ-RKvEE/s1600/tissue.png')")
# cur.execute("INSERT INTO goods VALUES ('ハンドソープ','人',3,3,'https://japaclip.com/files/hand-soap.png')")
# cur.execute("INSERT INTO goods VALUES ('ウェットティッシュ','物',1,1,'https://japaclip.com/files/hand-soap.png')")
# cur.execute("INSERT INTO noti VALUES ('noti1','ティッシュ',50,'U07ea05c326833f2183e0e37b70b59915',100)")
# cur.execute("INSERT INTO noti VALUES ('noti2','ハンドソープ',100,'aaaaa',100)")
conn.commit()

def end():
    cur.close()
    conn.close()

def templeteList():
    cur.execute("SELECT * FROM templete")
    templete_list = cur.fetchall()
    print(templete_list)
    return templete_list

def initilRegister(noti_name):
    cur.execute(f"INSERT INTO noti VALUES ({noti_name})")

def setList(goods_name,user_id,noti_name):
    cur.execute("SELECT * FROM templete WHERE goods_name=%s",(f'{goods_name}',))
    select_templete = cur.fetchall()
    cur.execute(f"INSERT INTO goods VALUES {select_templete} ")
    cur.execute(f"INSERT INTO noti VALUES (,{select_templete[0]},{select_templete[2]},{select_templete[0]},{user_id},{select_templete[2]}) WHERE noti_name=%s",(f'{noti_name}',)")
    print(select_templete)
    # return select_templete

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

def reduceGoods(noti_name):
    cur.execute("SELECT now-1 FROM noti WHERE noti_name=%s",(f'{noti_name}',))
    now = cur.fetchall()
    cur.execute(f"UPDATE noti SET now={now[0][0]} WHERE noti_name=%s",(f'{noti_name}',))
    cur.execute("SELECT now/capacity>0.2 FROM noti WHERE noti_name=%s",(f'{noti_name}',))
    ratio = cur.fetchall()
    print(ratio)
    return ratio[0][0]

def exchange(noti_name):
    cur.execute("SELECT goods_name FROM noti WHERE noti_name=%s",(f'{noti_name}',))
    name = cur.fetchall()
    cur.execute("SELECT stock-1 FROM goods WHERE goods_name=%s",(f'{name[0][0]}',))
    stock = cur.fetchall()
    cur.execute(f"UPDATE goods SET stock={stock[0][0]} WHERE goods_name=%s",(f'{name[0][0]}',))
    cur.execute("SELECT stock<2 FROM goods WHERE goods_name=%s",(f'{name[0][0]}',))
    ratio = cur.fetchall()
    return ratio[0][0],stock[0][0]

def now_reset(noti_name):
    cur.execute("SELECT capacity FROM noti WHERE noti_name=%s",(f'{noti_name}',))
    max = cur.fetchall()
    cur.execute(f"UPDATE noti SET stock={max[0][0]} WHERE goods_name=%s",(f'{noti_name}',))
