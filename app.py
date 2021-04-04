from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

# MessageEvent: 收到訊息的處理器
# TextMessage: 接收使用者文字訊息的處理器
# StickerMessage: 接收使用者貼圖訊息的處理器
# TextSendMessage: 回傳文字訊息的處理器
from linebot.models import (
    MessageEvent, TextMessage, StickerMessage, TextSendMessage, StickerSendMessage
)

# 引用爬蟲
from scraper import get_exchange_rate

def reply_exchange_rate(name):
    try : 
        exchange_rate = get_exchange_rate()
        bids = exchange_rate[name]["bids"]
        offers = exchange_rate[name]["offers"]
        reply_stream = "{}:\n買價 : {}\n賣價 : {}".format(name, bids, offers) 
        return reply_stream
    except :
        return "格式錯誤\n請輸入欲查詢之貨幣名稱\n(可輸入幣別如下\n美金\n港幣\n英鎊\n澳幣\n加拿大幣\n新加坡幣\n瑞士法郎\n日圓\n南非幣\n瑞典幣\n紐元\n泰幣\n菲國比索\n印尼幣\n歐元\n韓元\n越南盾\n馬來幣\n人民幣)\n如由疑問或找到程式漏洞\n請不要來找我"
app = Flask(__name__)
print("[程式開始運行]")

CHANNEL_ACCESS_TOKEN = 'mXM3E1PJFj989jfxmbjA9HO48w4DZ8tdSfWq0lvRfxiCHFOf1VLWBGvuuMBcRHL+8MzVFCqlpVe7ZjOj1CXd6aNG7fSDl7L0Q7/DhGchV48TAXpPJVdzMMDogqrvaqt2G7qZlZaG/Z5uzo9aDDbwEAdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '67d75e540cb93d3dc15ed89dd78a2613'


# ================== 以下為 X-LINE-SIGNATURE 驗證程序 ==================

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    print('[REQUEST]')
    print(request)
    print('[SIGNATURE]')
    print(signature)
    body = request.get_data(as_text=True)
    print("[BODY]")
    print(body)
    app.logger.info("Request body: " + body)
    try:
        print('[try]')
        handler.handle(body, signature)
    except InvalidSignatureError:
        print('[except]')
        abort(400)

    return 'OK'

# ================== 以上為 X-LINE-SIGNATURE 驗證程序 ==================

import os
if __name__ == "__main__":
    print('[伺服器開始運行]')
    # 取得遠端環境使用的連接端口，若是在本機端測試則預設開啟於port8080
    port = int(os.environ.get('PORT', 8080))
    # 使app開始在此連接端口上運行
    print('[預計運行於連接端口:{}]'.format(port))
    app.run(host='0.0.0.0', port=port)
