from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('gFmai/PVSPF5WWd/yS1iAe/GE4HbNjfysu32QO+Mmq3BNU1l9bAFoV/8Icqw0caMH1zUXE+VOzyjz9sK1+A1IIsPtouInOLk9xnmC9m3HgtA0Gqb3qt5DjVddvQtC4KwvxQxELGLVjA5iBSfZ8h5PQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('80a8ab90e63b617cccade125fe363b80')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()