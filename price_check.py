import os
import requests
import json

# --- [사령관님 설정 구역] ---
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
HISTORY_FILE = "last_price.txt"

TARGET_PRICE_1 = 75200  # 1차 거미줄 (체결 완료 지점!)
TARGET_PRICE_2 = 72500  # 2차 거미줄
TARGET_PRICE_3 = 69800  # 3차 거미줄
# ---------------------------

def get_btc_price_upbit():
    try:
        url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
        response = requests.get(url)
        return response.json()[0]['trade_price']
    except Exception as e:
        print(f"업비트 API 오류: {e}")
        return 0

def get_btc_price_usd():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url, timeout=10)
        return response.json()['bitcoin']['usd']
    except Exception as e:
        print(f"해외 API 오류: {e}")
        return 0.0

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
        response = requests.post(url, json=payload, timeout=10)
        print(f"텔레그램 응답: {response.status_code}")
    except Exception as e:
        print(f"텔레그램 발송 오류: {e}")

def run_logic():
    current_price_krw = get_btc_price_upbit()
    current_price_usd = get_btc_price_usd()
    
    if current_price_krw == 0 or current_price_usd == 0:
        return

    krw_formatted = format(int(current_price_krw), ',')
    usd_formatted = format(current_price_usd, ',.0f')
    
    fishing_report = ""
    if current_price_usd <= TARGET_PRICE_3:
        fishing_report = "🚨 [긴급: 3차 거미줄!] 시베리아 기단! 🥶"
    elif current_price_usd <= TARGET_PRICE_2:
        fishing_report = "🛒 [알림: 2차 거미줄!] 메인 쇼핑 타임!"
    elif current_price_usd <= TARGET_PRICE_1:
        fishing_report = "🕸️ [주의: 1차 거미줄!] 어제 잡은 그 가격대입니다!"

    message = (f"📢 *[비트코인 글로벌 보고]*\n"
               f"🇰🇷 업비트: `{krw_formatted}원`\n"
               f"🇺🇸 해외가: `${usd_formatted}`\n"
               f"🧙‍♂️✨🌳 행운이 팡팡! 🔥🍀🚀")

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            content = f.read().strip()
            last_price = float(content) if content else current_price_krw
        
        change_rate = ((current_price_krw - last_price) / last_price) * 100
        
        if abs(change_rate) >= 3 or fishing_report != "":
            emoji = "🚀 급등!!" if change_rate > 0 else "📉 급락!!"
            message = (f"🚨 *[사령관님 비밀 무전!]*\n"
                       f"------------------------\n"
                       f"{fishing_report if fishing_report else '⚠️ 변동성 감지!'}\n"
                       f"📈 변동률: `{change_rate:.2f}%` {emoji}\n"
                       f"------------------------\n"
                       f"사령관님, 즉시 전황판을 확인하십시오!!!")

    with open(HISTORY_FILE, "w") as f:
        f.write(str(current_price_krw))
        
    send_telegram_message(message)

if __name__ == "__main__":
    run_logic()
