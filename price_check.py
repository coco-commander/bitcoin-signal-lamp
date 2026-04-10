import requests

# [필독] 사령관님의 전용 정보로 교체하세요!
TELEGRAM_TOKEN = "8293408392:AAEsP67r6Z7xSvkiJQjDmkmz8pCm8LRidGY"
CHAT_ID = "8651989633"

def get_btc_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url)
    data = response.json()
    return float(data['price'])

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)

# 1. 가격 가져오기
price = get_btc_price()
formatted_price = "{:,.2f}".format(price)

# 2. 보고서 작성 (소고기 멘트 추가! ㅋㅋㅋ)
report = f"📢 [비트코인 승전보]\n사령관님! 현재 BTC 가격은 ${formatted_price}입니다.\n오늘도 소고기 파워로 화이팅입니다! 🥩🚀"

# 3. 텔레그램으로 전송
send_telegram_message(report)

# 4. 수첩(history.txt)에도 기록
with open("history.txt", "a") as f:
    f.write(f"{formatted_price}\n")

print("보고 완료!")
