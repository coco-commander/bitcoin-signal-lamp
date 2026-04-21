import os
import requests
import json

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# 가격 정보를 가져오는 함수들
def get_crypto_prices():
    try:
        # 코인게코 API 하나로 비트와 렌더 가격을 동시에 가져옵니다! ㅉㅉㅉ!
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,render-token&vs_currencies=usd,krw"
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        print(f"API 호출 오류: {e}")
        return None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

def run_logic():
    data = get_crypto_prices()
    if not data: return

    # 1. 비트코인 데이터 정리
    btc_usd = data['bitcoin']['usd']
    btc_krw = data['bitcoin']['krw']
    
    btc_message = (f"📢 [비트코인 실시간 보고]\n"
                   f"🇰🇷 업비트 기준가: {format(int(btc_krw), ',')}원\n"
                   f"🇺🇸 해외 시세: ${format(btc_usd, ',.0f')}\n"
                   f"🚦 비트 신호등 확인 완료! ㅉㅉㅉ!")

    # 2. 렌더(RENDER) 데이터 정리
    render_usd = data['render-token']['usd']
    render_krw = data['render-token']['krw']
    
    render_message = (f"🔮 [렌더(RENDER) 실전 보고]\n"
                      f"🇰🇷 현재가: {format(int(render_krw), ',')}원\n"
                      f"🇺🇸 달러가: ${format(render_usd, ',.3f')}\n"
                      f"👀 사령관님, 째려보기 구간입니다!")

    # 각각 따로 전송 (메시지가 두 개로 나눠서 옵니다!)
    send_telegram_message(btc_message)
    send_telegram_message(render_message)

if __name__ == "__main__":
    run_logic()
