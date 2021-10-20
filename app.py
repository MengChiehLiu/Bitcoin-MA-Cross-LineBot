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

@app.route("/function")
def function():
    # get price from binance api
    client = Client()
    klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_4HOUR, "two week ago")   #次處可自行更改時間級別

    # function to calculate sma value
    def sma(n):
        return sum([float(k[4]) for k in klines[-n-1:-1]])/n

    # function to calculate previous sma value
    def prev_sma(n):
        return sum([float(k[4]) for k in klines[-n-2:-2]])/n

    # calculate sma 5 and 60
    sma60 = sma(60)
    sma5 = sma(5)

    # calculate previous sma 5 and 60
    psma60 = prev_sma(60)
    psma5 = prev_sma(5)

    # golden cross
    if sma5 > sma60 and psma5 < psma60:
        line_bot_api.push_message("U55cce311c3805b9fa42f53867bd5d88d", TextSendMessage(text='4hr flip to long'))
        return '4hr flip to long'
        
    # dead cross
    if sma5 < sma60 and psma5 > psma60:
        line_bot_api.push_message("U55cce311c3805b9fa42f53867bd5d88d", TextSendMessage(text='4hr flip to short'))
        return '4hr flip to short'

    # hold for short
    if sma5 < sma60 and psma5 < psma60:
        return 'hold short'

    # hold for long
    if sma5 > sma60 and psma5 > psma60:
        return 'hold long'


if __name__ == "__main__":
    app.run()
