# Bitcoin_MA_Cross_LineBot
4小時級別比特幣5MA-60MA均線交叉策略，於交叉時會透過LineBot提醒。

##  佈署教學

1. 創建LineBot並佈署上Heroku。  
LineBot 參考教學: https://github.com/hsuanchi/Flask-LINE-Bot-Heroku
2. 將你的 Channel access token 以及 Channel secret 輸入程式當中。
3. 將此程式佈署至Heroku。
4. 將官方帳號加為好友後在聊天室中輸入「UID」並將回傳結果輸入程式當中。
5. 再次佈署程式後即開始運作。
6. 於Heroku Scheduler中設定每4小時執行一次app.py。  
Heroku Scheduler 參考教學: https://elements.heroku.com/addons/scheduler
