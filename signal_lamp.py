import requests

# 🛰️ 1. 실시간 데이터 수집 (업비트 & 바이낸스)
def get_live_data():
    # [업비트] 비트코인 원화 가격
    upbit_btc_url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
    upbit_btc_res = requests.get(upbit_btc_url).json()
    upbit_price = upbit_btc_res[0]['trade_price']

    # [바이낸스] 실시간 호가 중간값 계산 (오차 제로)
    binance_url = "https://api.binance.com/api/v3/ticker/bookTicker?symbol=BTCUSDT"
    binance_res = requests.get(binance_url).json()
    binance_price = (float(binance_res['bidPrice']) + float(binance_res['askPrice'])) / 2

    # [실시간 테더 환율] 업비트 KRW-USDT 가격 활용
    upbit_usdt_url = "https://api.upbit.com/v1/ticker?markets=KRW-USDT"
    upbit_usdt_res = requests.get(upbit_usdt_url).json()
    real_exchange_rate = upbit_usdt_res[0]['trade_price']

    return upbit_price, binance_price, real_exchange_rate

# 🚦 2. 프리미엄 계산 및 신호등 판독
def run_live_traffic_light():
    try:
        upbit_price, binance_price, exchange_rate = get_live_data()
        
        # 해외 달러 가격을 현재 테더 환율로 환산
        converted_binance = binance_price * exchange_rate
        
        # 프리미엄 비율 (%) 계산
        premium = ((upbit_price - converted_binance) / converted_binance) * 100

        print("=" * 50)
        print("🛰️ AI 참모 네오의 실시간 프리미엄 관측기")
        print("=" * 50)
        print(f"📊 업비트 비트코인 : {upbit_price:,.0f} 원")
        print(f"📊 바이낸스 환산가 : {converted_binance:,.0f} 원")
        print(f"🌍 실시간 테더 환율 : {exchange_rate:,.1f} 원")
        print("-" * 50)
        print(f"📈 현재 프리미엄    : {premium:.2f} %")
        print("-" * 50)

        # [사령관의 행동 강령 판독]
        if premium >= 5.0:
            print("🔴 [빨간불] 시장 과열! 추격 매수 엄금, 관망하세요.")
        elif 0.0 <= premium < 5.0:
            print("🟡 [노란불] 정상 범위. 정해진 DCA를 집행하세요.")
        else:
            print("🟢 [초록불] 역프리미엄! 적극적으로 모아가기 좋은 적기입니다.")
        print("=" * 50)

    except Exception as e:
        print(f"⚠️ 데이터 연결 에러: {e}")

# 🚀 시스템 가동!
run_live_traffic_light()
