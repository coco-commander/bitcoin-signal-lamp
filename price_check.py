import os
import requests

# 1. 환경 설정 (보안 금고에서 비번 가져오기)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_coin_prices():
    # 코인게코 ID: bitcoin, render-token, ondo-finance, solana, sui
    ids = "bitcoin,render-token,ondo-finance,solana,sui"
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(f"데이터 수신 오류: {e}")
        return None

def get_btc_krw():
    # 사령관님의 본진, 업비트 비트코인 가격!
    try:
        url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
        return requests.get(url).json()[0]['trade_price']
    except:
        return 0

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def run_logic():
    prices = get_coin_prices()
    btc_krw = get_btc_krw()
    
    if not prices:
        return

    # 가격 데이터 추출 (소수점 셋째자리까지 예쁘게!)
    btc_usd = prices['bitcoin']['usd']
    rndr = prices['render-token']['usd']
    ondo = prices['ondo-finance']['usd']
    sol = prices['solana']['usd']
    sui = prices['sui']['usd']

    # 메시지 구성 (국기와 이모지로 시인성 극대화!)
    message = (
        f"🚀 *[알트코인 함대 통합 보고]* 🚀\n\n"
        f"🇰🇷 *BTC (업비트):* {btc_krw:,.0f}원\n"
        f"🇺🇸 *BTC (해외):* ${btc_usd:,.0f}\n"
        f"--------------------------\n"
        f"📽️ *RENDER:* ${rndr:.3f}\n"
        f"🌡️ *ONDO:* ${ondo:.3f}\n"
        f"☀️ *SOLANA:* ${sol:.2f}\n"
        f"💧 *SUI:* ${sui:.3f}\n\n"
        f"🧙‍♂️✨ 행운이 팡팡! 🔥🍀🚀"
    )

    send_telegram_message(message)

if __name__ == "__main__":
    run_logic()
