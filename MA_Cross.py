# get price from binance api
client = Client()
klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "one week ago")   #此處可自行調整時間級別

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
    line_bot_api.push_message("U55cce311c3805b9fa42f53867bd5d88d", TextSendMessage(text='1hr flip to long'))

# dead cross
if sma5 < sma60 and psma5 > psma60:
    line_bot_api.push_message("U55cce311c3805b9fa42f53867bd5d88d", TextSendMessage(text='1hr flip to short'))
