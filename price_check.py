import requests

# [필독] 사령관님의 정보를 아래 큰따옴표("") 안에 정확히 넣어주세요!
TELEGRAM_TOKEN = "8293408392:AAEsP67r6Z7xSvkiJQjDmkmz8pCm8LRidGY"
CHAT_ID = "8651989633"

def get_btc_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url)
    data = response.json()
    return float(data['price'])

def send_telegram_message(message):
    # 사령관님이 올려주신 그 완벽한 코드입니다! ㅉㅉㅉ!
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)

# --- 여기서부터 실행 ---
try:
    # 1. 가격 가져오기
    price = get_btc_price()
    formatted_price = "{:,.2f}".format(price)

    # 2. 보고서 작성
    report = f"📢 [비트코인 승전보]\n사령관님! 현재 BTC 가격은 ${formatted_price}입니다.\n오늘도 소고기 파워로 화이팅입니다! 🥩🚀"

    # 3. 텔레그램으로 전송
    send_telegram_message(report)
    
    # 4. 수첩 기록
    with open("history.txt", "a") as f:
        f.write(f"{formatted_price}\n")
    
    print("성공적으로 메시지를 보냈습니다!")

except Exception as e:
    print(f"오류 발생: {e}")
