import os  # 금고를 열기 위한 마법의 도구입니다!
import requests

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_btc_price_upbit():
    url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
    response = requests.get(url)
    data = response.json()
    return data[0]['trade_price']

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)


# --- 실제 실행 구간 ---
try:
    price_krw = get_btc_price_upbit()
    formatted_krw = "{:,.0f}".format(price_krw)
    
    # 보고서 작성 (원화 버전으로 업그레이드!)
    report_text = f"📢 [비트코인 업비트 승전보]\n사령관님! 현재 BTC 가격은 {formatted_krw}원입니다.\n행운이 팡팡 터집니다! 🥩🚀"
    
    # 텔레그램 발송
    send_telegram_message(report_text)
    
    # 수첩 기록
    with open("history.txt", "a") as f:
        f.write(f"KRW: {formatted_krw}\n")
        
    print("업비트 보고 성공!")
except Exception as e:
    print(f"사령관님, 새로운 에러 발생: {e}")
