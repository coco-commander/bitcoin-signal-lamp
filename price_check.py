import os
import requests
import json

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
HISTORY_FILE = "last_price.txt"  # 가격을 기억할 작은 수첩입니다

def get_btc_price_upbit():
    url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
    response = requests.get(url)
    return response.json()[0]['trade_price']

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

def run_logic():
    current_price = get_btc_price_upbit()
    price_formatted = format(int(current_price), ',')
    
    message = f"📢 [업비트 정기보고]\n현재 비트코인: {price_formatted}원입니다.\n🧙‍♂️✨🌳 행운이 팡팡! 🔥🍀🚀"
    
    # 1. 이전 가격 불러오기 (수첩 확인)
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            last_price = float(f.read())
        
        # 2. 가격 변동 계산 (변동률 %)
        change_rate = ((current_price - last_price) / last_price) * 100
        
        # 3. 만약 3% 이상 변했다면? (긴급 사이렌!)
        if abs(change_rate) >= 3:
            emoji = "🚀 급등!!" if change_rate > 0 else "📉 급락!!"
            message = f"🚨 사령관님, [긴급 상황 발생!]\n현재가: {price_formatted}원\n변동률: {change_rate:.2f}% {emoji}\n사령관님, 차트를 확인하십시오!"

    # 4. 새로운 가격을 수첩에 적기
    with open(HISTORY_FILE, "w") as f:
        f.write(str(current_price))
        
    # 5. 최종 메시지 전송
    send_telegram_message(message)

if __name__ == "__main__":
    run_logic()
