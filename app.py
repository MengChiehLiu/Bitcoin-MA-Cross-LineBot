from flask import Flask, request, abort
from binance.client import Client
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

line_bot_api = LineBotApi("") #輸入自己的
handler = WebhookHandler("")  #輸入自己的

app=Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello LineBot"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"

if __name__ == "__main__":
    app.run()
