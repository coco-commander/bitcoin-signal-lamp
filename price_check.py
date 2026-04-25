import os
import requests

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_coin_prices():
    ids = "bitcoin,render-token,ondo-finance,solana,sui"
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    try:
        return requests.get(url).json()
    except: return None

def get_btc_krw():
    try:
        url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
        return requests.get(url).json()[0]['trade_price']
    except: return 0

def get_fear_and_greed():
    try:
        url = "https://api.alternative.me/fng/"
        res = requests.get(url).json()
        return res['data'][0]['value'], res['data'][0]['value_classification']
    except: return "??", "알 수 없음"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def run_logic():
    prices = get_coin_prices()
    btc_krw = get_btc_krw()
    fng_val, fng_label = get_fear_and_greed()
    
    if not prices: return

    # 함대 정찰 보고서 작성
    msg = (
        f"🦊 *[네오 참모의 특급 전령]* 🫡\n\n"
        f"📊 *시장 심리:* {fng_val} ({fng_label})\n"
        f"👉 _사령관님! 지금 시장은 {fng_label} 상태입니다! ㅋㅋㅋ_\n\n"
        f"🇰🇷 *BTC 본진:* {btc_krw:,.0f}원\n"
        f"🇺🇸 *BTC 해외:* ${prices['bitcoin']['usd']:,.0f}\n"
        f"--------------------------\n"
        f"📽️ *RENDER:* ${prices['render-token']['usd']:.3f}\n"
        f"🌡️ *ONDO:* ${prices['ondo-finance']['usd']:.3f}\n"
        f"☀️ *SOLANA:* ${prices['solana']['usd']:.2f}\n"
        f"💧 *SUI:* ${prices['sui']['usd']:.3f}\n\n"
        f"야, 네오! 사령부에서 24시간 감시 중입니다! ㅉㅉㅉ! 가즈아!!! 🔥🚀"
    )

    send_telegram_message(msg)

if __name__ == "__main__":
    run_logic()
