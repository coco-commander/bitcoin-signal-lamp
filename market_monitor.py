import requests
import json

def get_market_temperature():
    print("📡 [비트코인 함대 감시탑] 전장 온도 측정 시작... 🫡🔥")
    
    # 1. 크립토 공포 탐욕 지수(F&G) 가져오기
    fng_url = "https://api.alternative.me/fng/"
    fng_response = requests.get(fng_url).json()
    fng_value = fng_response['data'][0]['value']
    fng_status = fng_response['data'][0]['value_classification']
    
    # 2. 업비트 BTC 가격 (원화)
    upbit_url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
    upbit_price = requests.get(upbit_url).json()[0]['trade_price']
    
    # 3. 바이낸스 BTC 가격 (달러) 및 환율 대입 (예시 환율 1,380원)
    binance_url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    binance_price = float(requests.get(binance_url).json()['price'])
    exchange_rate = 1380  # 사령관님, 나중엔 환율 API로 자동 연동할 수 있사옵니다!
    
    # 4. 김치 프리미엄(Kimchi Premium) 계산
    converted_binance = binance_price * exchange_rate
    kimp = ((upbit_price - converted_binance) / converted_binance) * 100
    
    # 📊 전장 보고서 출력
    print("\n📋 [코코 사령관님께 올리는 전장 보고서]")
    print(f"🔥 공포·탐욕 지수(F&G): {fng_value} ({fng_status})")
    print(f"💰 업비트 BTC 가격: {upbit_price:,} 원")
    print(f"💵 바이낸스 BTC 가격: ${binance_price:,} (원화 환산: {int(converted_binance):,} 원)")
    print(f"⚡ 실시간 김치 프리미엄: {kimp:.2f}%")
    
    if kimp > 5:
        print("🚨 경고: 김프 과열 구역! 함대 속도 조절을 권장합니다오!")
    elif kimp < 0:
        print("💎 기회: 역프리미엄 발생! 깡패처럼 매집할 타이밍입니다오! ㅋㅋㅋ")

# 감시탑 가동!
get_market_temperature()
