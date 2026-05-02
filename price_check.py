import os
import requests
import json

# --- [사령관님 설정 구역] ---
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
HISTORY_FILE = "last_price.txt"

# 사령관님의 거미줄 타겟가 (달러 기준) - 유령 공백 싹 제거 완료! ㅉㅉㅉ!
TARGET_PRICE_1 = 75200
TARGET_PRICE_2 = 72500
TARGET_PRICE_3 = 69800
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
        # 코인게코가 가끔 응답이 늦을 때를 대비해 타임아웃 추가!
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
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"텔레그램 발송 오류: {e}")

def run_logic():
    current_price_krw = get_btc_price_upbit()
    current_price_usd = get_btc_price_usd()
    
    if current_price_krw == 0 or current_price_usd == 0:
        print("데이터를 가져오는 데 실패했습니다.")
        return

    krw_formatted = format(int(current_price_krw), ',')
    usd_formatted = format(current_price_usd, ',.0f')
    
    fishing_report = ""
    if current_price_usd <= TARGET_PRICE_3:
        fishing_report = "🚨 [긴급: 3차 거미줄 구역 돌입!] 시베리아 기단 도착! 🥶"
    elif current_price_usd <= TARGET_PRICE_2:
        fishing_report = "🛒 [알림: 2차 거미줄 체결 중!] 메인 쇼핑 타임입니다!"
    elif current_price_usd <= TARGET_PRICE_1:
        fishing_report = "🕸️ [주의: 1차 거미줄 작동!] 꽃샘추위가 시작됐습니다!"

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
            message = (f"🚨 *[사령관님 비상 무전!]*\n"
                       f"------------------------\n"
                       f"{fishing_report if fishing_report else '⚠️ 변동성 감지!'}\n"
                       f"🇰🇷 현재가: `{krw_formatted}원`\n"
                       f"🇺🇸 해외가: `${usd_formatted}`\n"
                       f"📈 변동률: `{change_rate:.2f}%` {emoji}\n"
                       f"------------------------\n"
                       f"사령관님, 즉시 전황판을 확인하십시오!!!")

    with open(HISTORY_FILE, "w") as f:
        f.write(str(current_price_krw))
        
    send_telegram_message(message)

if __name__ == "__main__":
    run_logic()
