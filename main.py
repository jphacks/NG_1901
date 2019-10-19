from flask import Flask, request, abort
import os
import noti_db

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    CarouselColumn, CarouselTemplate, ImageMessage,
    MessageEvent, TemplateSendMessage, TextMessage,
    TextSendMessage, URITemplateAction,ButtonsTemplate,URIAction
)

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

# 回数
@app.route("/count", methods=['GET'])
def count():
    count = request.args.get('count')
    print(count)
    return count

@app.route("/distance", methods=['GET'])
def distance():
    #設定完了したよ！通知
    print("ok")
    return "ok"

def push():

    url = 'https://api.line.me/v2/bot/message/push'
    data = {
        "to": "",
        "messages": [
            {
                "type": "text",
                "text": "Hello, user!"
            }
        ]
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + YOUR_CHANNEL_ACCESS_TOKEN
    }
    requests.post(url, data=json.dumps(data), headers=headers)


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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if '登録' in event.message.text:
        content = 'notiのボタンを長押ししてください。'
        # notes = [
        #     CarouselColumn(
        #                     image_background_color='#FFFFFF',
        #                     # title='Noti1',
        #                     text='Noti1',
        #                     actions=[{'type': 'message','label': 'これにする','text': '登録完了'}]),
        #
        #     CarouselColumn(
        #                     image_background_color='#FFFFFF',
        #                     # title='Noti1',
        #                     text='Noti2',
        #                     actions=[{'type': 'message','label': 'これにする','text': '登録完了'}]),
        #
        #     CarouselColumn(
        #                     image_background_color='#FFFFFF',
        #                     # title='Noti1',
        #                     text='Noti3',
        #                     actions=[{'type': 'message','label': 'これにする','text': '登録完了'}])]
        #
        # messages = TemplateSendMessage(
        #     alt_text='template',
        #     template=CarouselTemplate(columns=notes),
        # )
        line_bot_api.reply_message(event.reply_token, messages=messages)
    elif 'リスト' in event.message.text:
        list = noti_db.list()
        notes = [
            CarouselColumn(
                            thumbnail_image_url='https://1.bp.blogspot.com/-dncnFat-Kf8/UV1JSxgmdaI/AAAAAAAAPXo/0aloQ-RKvEE/s1600/tissue.png',
                            image_background_color='#FFFFFF',
                            title=f'{list[0][0]}',
                            text=f'在庫：{list[0][2]}',
                            actions=[{'type': 'message','label': '購入','text': '購入'}]),

            CarouselColumn(
                            thumbnail_image_url='https://japaclip.com/files/hand-soap.png',
                            image_background_color='#FFFFFF',
                            title=f'{list[1][0]}',
                            text=f'在庫：{list[0][2]}',
                            actions=[{'type': 'message','label': '購入','text': '購入'}]),

            CarouselColumn(
                            thumbnail_image_url='',
                            image_background_color='#a9a9a9',
                            title=f'{list[2][0]}',
                            text=f'在庫：{list[0][2]}',
                            actions=[{'type': 'message','label': '購入','text': '購入'}])]

        messages = TemplateSendMessage(
            alt_text='template',
            template=CarouselTemplate(columns=notes),
        )
        line_bot_api.reply_message(event.reply_token, messages=messages)
    elif 'Noti' in event.message.text:
        content = 'You can do it.'
    elif '確認' in event.message.text:
        notes = [
            CarouselColumn(
                            image_background_color='#FFFFFF',
                            # title='Noti1',
                            text='Noti1',
                            actions=[{'type': 'message','label': '確認','text': '確認'}]),

            CarouselColumn(
                            image_background_color='#FFFFFF',
                            # title='Noti1',
                            text='Noti2',
                            actions=[{'type': 'message','label': '確認','text': '確認'}]),

            CarouselColumn(
                            image_background_color='#FFFFFF',
                            # title='Noti1',
                            text='Noti3',
                            actions=[{'type': 'message','label': '確認','text': '確認'}])]

        messages = TemplateSendMessage(
            alt_text='template',
            template=CarouselTemplate(columns=notes),
        )
        line_bot_api.reply_message(event.reply_token, messages=messages)
    else:
        content = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f'{content}'))

if __name__ == "__main__":
#    app.run()
    noti_db.initialization()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
