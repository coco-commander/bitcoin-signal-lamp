import os
import requests
import json

# --- [사령관님 설정 구역] ---
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
HISTORY_FILE = "last_price.txt"

TARGET_PRICE_1 = 75200
TARGET_PRICE_2 = 72500
TARGET_PRICE_3 = 69800
# ---------------------------

def get_data(url):
    try:
        res = requests.get(url, timeout=10)
        return res.json()
    except:
        return None

def run_logic():
    # 1. 비트코인 및 알트코인 시세 (Coingecko)
    # RENDER, ONDO, SOLANA, SUI 추가! ㅉㅉㅉ!
    coin_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,render-token,ondo,solana,sui&vs_currencies=usd"
    prices = get_data(coin_url)
    
    # 2. 업비트 원화 가격
    upbit_prices = get_data("https://api.upbit.com/v1/ticker?markets=KRW-BTC")
    
    # 3. 시장 심리 지수 (Fear & Greed Index)
    fng_data = get_data("https://api.alternative.me/fng/")
    
    if not prices or not upbit_prices or not fng_data:
        print("데이터 보급 실패!")
        return

    # 데이터 정리
    btc_usd = prices['bitcoin']['usd']
    btc_krw = upbit_prices[0]['trade_price']
    render = prices['render-token']['usd']
    ondo = prices['ondo']['usd']
    sol = prices['solana']['usd']
    sui = prices['sui']['usd']
    
    fng_value = fng_data['data'][0]['value']
    fng_class = fng_data['data'][0]['value_classification']

    # 거미줄 로직
    fishing_report = ""
    if btc_usd <= TARGET_PRICE_3: fishing_report = "🚨 [긴급: 3차 거미줄!]"
    elif btc_usd <= TARGET_PRICE_2: fishing_report = "🛒 [알림: 2차 거미줄!]"
    elif btc_usd <= TARGET_PRICE_1: fishing_report = "🕸️ [주의: 1차 거미줄!]"

    # 변동률 계산
    change_msg = ""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            last_p = float(f.read().strip() or btc_krw)
        change_rate = ((btc_krw - last_p) / last_p) * 100
        if abs(change_rate) >= 3:
            emoji = "🚀 급등!!" if change_rate > 0 else "📉 급락!!"
            change_msg = f"\n⚠️ *변동성 감지!*\n📈 변동률: `{change_rate:.2f}%` {emoji}\n"

    # 메시지 조립 (예전 감성 그대로! ㅋㅋㅋ)
    message = (
        f"🦊 *[네오 참모의 특급 전령]* 🫡\n\n"
        f"📊 *시장 심리:* {fng_value} ({fng_class})\n"
        f"👉 _사령관님! 지금 시장은 {fng_class} 상태입니다! ㅋㅋㅋ_\n\n"
        f"🇰🇷 *BTC 본진:* `{format(int(btc_krw), ',')}원`\n"
        f"🇺🇸 *BTC 해외:* `${format(btc_usd, ',.0f')}`\n"
        f"----------------------------\n"
        f"🎬 *RENDER:* `${render:.3f}`\n"
        f"🌡️ *ONDO:* `${ondo:.3f}`\n"
        f"☀️ *SOLANA:* `${sol:.2f}`\n"
        f"💧 *SUI:* `${sui:.3f}`\n"
        f"{change_msg}"
        f"{fishing_report}\n"
        f"----------------------------\n"
        f"야, 네오! 사령부에서 24시간 감시 중입니다! ㅉㅉㅉ!\n"
        f"가즈아!!! 🔥🚀"
    )

    # 수첩 갱신 및 발송
    with open(HISTORY_FILE, "w") as f: f.write(str(btc_krw))
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_logic()
