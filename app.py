from flask import Flask, request, abort
from binance.client import Client
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

line_bot_api = LineBotApi("") # 輸入自己的 Channel access token
handler = WebhookHandler("")  # 輸入自己的 Channel secret
MyUID = ""                    # 輸入自己的 UID


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
    klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_4HOUR, "two week ago")
    dropdown = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "15m ago")[0]

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

    # dropdown alert
    open_price = float(dropdown[1])
    now_price = float(dropdown[4])
    if (open_price - now_price) >= 500:
        line_bot_api.push_message(MyUID, TextSendMessage(text='Alert!!! Big Dropdown!'))

    # golden cross
    if sma5 > sma60 and psma5 < psma60:
        line_bot_api.push_message(MyUID, TextSendMessage(text='4hr flip to long'))
        return '4hr flip to long'
        
    # dead cross
    if sma5 < sma60 and psma5 > psma60:
        line_bot_api.push_message(MyUID, TextSendMessage(text='4hr flip to short'))
        return '4hr flip to short'

    # hold for short
    if sma5 < sma60 and psma5 < psma60:
        return 'hold short'

    # hold for long
    if sma5 > sma60 and psma5 > psma60:
        return 'hold long'

@handler.add(MessageEvent, message=TextMessage)
def talk(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    user_id = profile.user_id
    if event.message.text == "UID":
        try:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=user_id))
        except:
            pass

if __name__ == "__main__":
    app.run()
