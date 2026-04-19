import os
import requests
import json

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
HISTORY_FILE = "last_price.txt"

# 1. 업비트 원화 가격 가져오기 (사령관님 본진)
def get_btc_price_upbit():
    try:
        url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
        response = requests.get(url)
        return response.json()[0]['trade_price']
    except Exception as e:
        print(f"업비트 API 오류: {e}")
        return 0

# 2. 해외 실제 달러 가격 직접 가져오기 (오차 방지)
def get_btc_price_usd():
    try:
        # 코인게코 API를 통해 실제 해외 달러 시세를 가져옵니다. ㅉㅉㅉ!
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url)
        return response.json()['bitcoin']['usd']
    except Exception as e:
        print(f"해외 API 오류: {e}")
        return 0.0

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

def run_logic():
    # 데이터 수집
    current_price_krw = get_btc_price_upbit()
    current_price_usd = get_btc_price_usd()
    
    if current_price_krw == 0 or current_price_usd == 0:
        print("데이터를 가져오는 데 실패했습니다.")
        return

    # 예쁘게 숫자 포맷팅
    krw_formatted = format(int(current_price_krw), ',')
    usd_formatted = format(current_price_usd, ',.0f') # 달러도 깔끔하게 정수로!
    
    # 기본 메시지 구성 (국기 추가로 시인성 UP!)
    message = (f"📢 [비트코인 글로벌 보고]\n"
               f"🇰🇷 업비트: {krw_formatted}원\n"
               f"🇺🇸 해외가: ${usd_formatted}\n"
               f"🧙‍♂️✨🌳 행운이 팡팡! 🔥🍀🚀")

    # 가격 변동 체크 (수첩 확인)
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            last_price = float(f.read())
        
        change_rate = ((current_price_krw - last_price) / last_price) * 100
        
        # 3% 이상 변동 시 긴급 사이렌!
        if abs(change_rate) >= 3:
            emoji = "🚀 급등!!" if change_rate > 0 else "📉 급락!!"
            message = (f"🚨 사령관님, [긴급 상황 발생!]\n"
                       f"🇰🇷 현재가: {krw_formatted}원\n"
                       f"🇺🇸 해외가: ${usd_formatted}\n"
                       f"📈 변동률: {change_rate:.2f}% {emoji}\n"
                       f"사령관님, 차트를 확인하십시오!")

    # 새로운 가격을 수첩에 저장
    with open(HISTORY_FILE, "w") as f:
        f.write(str(current_price_krw))
        
    # 최종 전송
    send_telegram_message(message)

if __name__ == "__main__":
    run_logic()
