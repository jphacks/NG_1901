from flask import Flask, request, abort
import os
import noti_db
import noti_purchase.get_amazon_url
amazon = noti_purchase.get_amazon_url

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    CarouselColumn, CarouselTemplate, ImageMessage,
    MessageEvent, TemplateSendMessage, TextMessage, FollowEvent,
    TextSendMessage, URITemplateAction,ButtonsTemplate,URIAction
)

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# 検証用
# noti = 'noti1'

@app.route("/")
def hello_world():
    return "hello world!"

# 初期登録
@app.route("/registration", methods=['GET'])
def registration():
    noti = request.args.get('noti')
    temp = noti_db.selectUserId(noti)
    # テンプレートから選択
    list = noti_db.templeteList()
    notes = [
        CarouselColumn(
                        thumbnail_image_url=f'{list[0][4]}',
                        image_background_color='#FFFFFF',
                        text=f'{list[0][0]}',
                        actions=[{'type': 'message','label': '登録','text': f'登録：{list[0][0]}'}]),

        CarouselColumn(
                        thumbnail_image_url=f'{list[1][4]}',
                        image_background_color='#FFFFFF',
                        text=f'{list[1][0]}',
                        actions=[{'type': 'message','label': '登録','text': f'登録：{list[1][0]}'}]),

        CarouselColumn(
                        thumbnail_image_url='https://i1.wp.com/sozaikoujou.com/wordpress/wp-content/uploads/2016/06/th_app_button_plus.jpg?w=600&ssl=1',
                        image_background_color='#FFFFFF',
                        text=f'{list[2][0]}',
                        actions=[{'type': 'message','label': '登録','text': f'登録：{list[2][0]}'}])]

    messages = TemplateSendMessage(
        alt_text='template',
        template=CarouselTemplate(columns=notes),
    )
    text = '対象を選択してください。'
    sendCarouselMessage(temp,messages)
    sendMessage(temp,text)
    return "ok"

# センサ距離の調整
@app.route("/distance", methods=['GET'])
def distance():
    print("ok")
    return "ok"

# 消耗品を使用したかの確認
@app.route("/count", methods=['GET'])
def count():
    # 残量減らす
    jadge = noti_db.reduceGoods('noti1')
    print(jadge)
    noti_db.exchange('noti1')
    if jadge == True:
        temp = noti_db.selectUserId('noti1')
        text = '残量が減ってきました。残りの在庫は2つです。'
        sendCarouselMessage(temp,messages)
        sendMessage(temp,text)
    return "ok"

# ものに反応した時の通知
@app.route("/object", methods=['GET'])
def object():
    noti = request.args.get('noti')
    temp = noti_db.selectUserId(noti)
    text = '反応がありました。'
    sendMessage(temp,text)
    return "ok"

# 交換した時の残量リセットと在庫通知
@app.route("/exchange", methods=['GET'])
def exchange():
    noti = request.args.get('noti')
    jadge = noti_db.exchange(noti)
    if jadge[0] == True:
        temp = noti_db.selectUserId(noti)
        text = f'交換しました。残りの在庫は{jadge[1]}つです。'
        sendMessage(temp,text)
        noti_db.now_reset(noti)
    return "ok"

# LINE認証
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 友達追加時イベント
@handler.add(FollowEvent)
def on_follow(event):
    user_id = event.source.user_id
    reply_token = event.reply_token
    noti_db.registerId(user_id,reply_token)

# 返信イベント
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if '登録' == event.message.text:
        content = 'notiのボタンをランプが黄色に点灯するまで長押ししてください。'

    elif 'リスト' in event.message.text:
        list = noti_db.goodsList()
        result = amazon.search_amazon('ティッシュ')
        notes = [
            CarouselColumn(
                            thumbnail_image_url=f'{list[0][4]}',
                            image_aspect_ratio='square',
                            image_size='contain',
                            image_background_color='#FFFFFF',
                            title=f'{list[0][0]}',
                            text=f'在庫：{list[0][2]}',
                            actions=[{'type': 'message','label': '購入','text': f'{result}'}]),

            CarouselColumn(
                            thumbnail_image_url=f'{list[1][4]}',
                            image_aspect_ratio='square',
                            image_size='contain',
                            image_background_color='#FFFFFF',
                            title=f'{list[1][0]}',
                            text=f'在庫：{list[1][2]}',
                            actions=[{'type': 'message','label': '購入','text': 'a'}])

            # CarouselColumn(
            #                 thumbnail_image_url='https://i1.wp.com/sozaikoujou.com/wordpress/wp-content/uploads/2016/06/th_app_button_plus.jpg?w=600&ssl=1',
            #                 image_aspect_ratio='square',
            #                 image_size='contain',
            #                 image_background_color='#FFFFFF',
            #                 title=f'{list[2][0]}',
            #                 text=f'在庫：{list[2][2]}',
            #                 actions=[{'type': 'message','label': '購入','text': 'a'}])
                            ]

        messages = TemplateSendMessage(
            alt_text='template',
            template=CarouselTemplate(columns=notes),
        )
        line_bot_api.reply_message(event.reply_token, messages=messages)
    elif 'noti' in event.message.text:
        content = 'You can do it.'
    elif 'ヘルプ' in event.message.text:
        content = '''【登録】
使用するnotiの設定，登録を行うことができます．
①noti選択
②対象選択
③用途の選択
④実際の使用環境情報の設定
上記を順に行い，詳細は各項目ごとに説明します．
※テンプレートを選択すると③，④は省略されます．
【リスト】
管理している対象のリストを返します．
内容には，
①対象名
②在庫
が含まれます．
【通知】
対象物の残量や在庫が無くなりそうな場合，自動で通知がきます．'''
    else:
        print('ok')
        # content = event.message.text

    if '登録：' in event.message.text:
        temp = noti_db.selectUserId(noti)
        noti_db.setList(event.message.text[3:],temp,event.source.user_id)
        content = '登録完了'


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f'{content}'))

# テキストメッセージの送信
def sendMessage(user_id,text):
    line_bot_api.push_message(
        user_id,
        messages=TextSendMessage(text=text)
    )

# カルーセルメッセージの送信
def sendCarouselMessage(user_id,messages):
    line_bot_api.push_message(
        user_id,
        messages=messages
    )

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
