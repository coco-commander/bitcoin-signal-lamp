import os
import requests
import json

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
HISTORY_FILE = "last_price.txt"

# [비책 1] 실시간 환율 정보 가져오기 함수 추가!
def get_usd_krw_exchange_rate():
    try:
        # 무료 환율 API를 사용하거나, 고정값(예: 1350)을 써도 되지만 
        # 일단은 가장 간단하게 다른 API에서 환율을 슥~ 가져오는 로직입니다.
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url)
        return response.json()['rates']['KRW']
    except:
        return 1350.0  # 혹시 API가 응답 없으면 기본 환율로 대응! (철저한 대비 ㅋㅋㅋ)

def get_btc_price_upbit():
    url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
    response = requests.get(url)
    return response.json()[0]['trade_price']

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

def run_logic():
    # 1. 원화 가격 가져오기
    current_price_krw = get_btc_price_upbit()
    
    # 2. 환율 가져와서 달러 가격 계산하기
    exchange_rate = get_usd_krw_exchange_rate()
    current_price_usd = current_price_krw / exchange_rate
    
    # [비책 2] 예쁘게 포맷팅하기
    krw_formatted = format(int(current_price_krw), ',')
    usd_formatted = format(current_price_usd, ',.2f') # 소수점 2자리까지!
    
    message = (f"📢 [업비트 글로벌 보고]\n"
               f"🇰🇷 원화: {krw_formatted}원\n"
               f"🇺🇸 달러: ${usd_formatted}\n"
               f"(적용환율: {exchange_rate}원)\n"
               f"🧙‍♂️✨🌳 행운이 팡팡! 🔥🍀🚀")

    # [이후 변동 계산 로직은 기존과 동일...]
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            last_price = float(f.read())
        
        change_rate = ((current_price_krw - last_price) / last_price) * 100
        
        if abs(change_rate) >= 3:
            emoji = "🚀 급등!!" if change_rate > 0 else "📉 급락!!"
            message = (f"🚨 사령관님, [긴급 상황!]\n"
                       f"💰 현재가: {krw_formatted}원 (${usd_formatted})\n"
                       f"📈 변동률: {change_rate:.2f}% {emoji}\n"
                       f"사령관님, 차트를 확인하십시오!")

    with open(HISTORY_FILE, "w") as f:
        f.write(str(current_price_krw))
        
    send_telegram_message(message)

if __name__ == "__main__":
    run_logic()
