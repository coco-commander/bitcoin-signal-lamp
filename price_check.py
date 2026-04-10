import requests

# [여기에 사령관님의 정보 입력]
TELEGRAM_TOKEN = "8293408392:AAEsP67r6Z7xSvkiJQjDmkmz8pCm8LRidGY"
CHAT_ID = "8651989633"

def get_btc_price_upbit():
    # 업비트 기지는 깃허브 로봇을 환영합니다! ㅋㅋㅋ
    url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
    response = requests.get(url)
    data = response.json()
    # 업비트는 KRW(원화) 기준이므로 달러($) 느낌을 내기 위해 1350으로 나눕니다! ㅋㅋㅋ
    price_krw = data[0]['trade_price']
    return price_krw

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

# --- 실제 실행 구간 ---
try:
    price_krw = get_btc_price_upbit()
    formatted_krw = "{:,.0f}".format(price_krw)
    
    # 보고서 작성 (원화 버전으로 업그레이드!)
    report_text = f"📢 [비트코인 업비트 승전보]\n사령관님! 현재 BTC 가격은 {formatted_krw}원입니다.\n한국인의 힘! 소고기 가즈아! 🥩🚀"
    
    # 텔레그램 발송
    send_telegram_message(report_text)
    
    # 수첩 기록
    with open("history.txt", "a") as f:
        f.write(f"KRW: {formatted_krw}\n")
        
    print("업비트 보고 성공!")
except Exception as e:
    print(f"사령관님, 새로운 에러 발생: {e}")
