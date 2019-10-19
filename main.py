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

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/count", methods=['GET'])
def count():
    return "ok"

@app.route("/distance", methods=['GET'])
def distance():
    print("ok")
    return "ok"

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

# Follow Event
@handler.add(FollowEvent)
def on_follow(event):
    user_id = event.source.user_id
    reply_token = event.reply_token
    noti_db.register_id(user_id,reply_token)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if '登録' in event.message.text:
        content = 'notiのボタンを長押ししてください。'
        noti_db.templeteList()

    elif 'リスト' in event.message.text:
        list = noti_db.goodsList()
        notes = [
            CarouselColumn(
                            thumbnail_image_url=f'{list[0][4]}',
                            image_aspect_ratio='square',
                            image_size='contain',
                            image_background_color='#FFFFFF',
                            title=f'{list[0][0]}',
                            text=f'在庫：{list[0][2]}',
                            actions=[{'type': 'message','label': '購入','text': 'aa']),

            CarouselColumn(
                            thumbnail_image_url=f'{list[1][4]}',
                            image_aspect_ratio='square',
                            image_size='contain',
                            image_background_color='#FFFFFF',
                            title=f'{list[1][0]}',
                            text=f'在庫：{list[1][2]}',
                            actions=[{'type': 'message','label': '購入','text': '購入'}]),

            CarouselColumn(
                            thumbnail_image_url='https://i1.wp.com/sozaikoujou.com/wordpress/wp-content/uploads/2016/06/th_app_button_plus.jpg?w=600&ssl=1',
                            image_aspect_ratio='square',
                            image_size='contain',
                            image_background_color='#FFFFFF',
                            title=f'{list[2][0]}',
                            text=f'在庫：{list[2][2]}',
                            actions=[{'type': 'message','label': '購入','text': '購入'}])]

        messages = TemplateSendMessage(
            alt_text='template',
            template=CarouselTemplate(columns=notes),
        )
        line_bot_api.reply_message(event.reply_token, messages=messages)
    elif 'noti' in event.message.text:
        content = 'You can do it.'
    elif 'ヘルプ' in event.message.text:
        content = '自分の心に聞くんだ'
    else:
        content = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f'{content}'))

# メッセージの送信
def sendMessage(reply_token,text):
    line_bot_api.reply_message(
        reply_token=reply_token,
        messages=TextSendMessage(text=text)
    )

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
