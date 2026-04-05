import requests

def get_market_data():
    try:
        print("-" * 40)
        print(f"🚀 [시스템 사령관 코코의 마켓 센티넬 가동]")
        print("-" * 40)

        # 1. 환율 가져오기
        try:
            ex_url = "https://api.exchangerate-api.com/v4/latest/USD"
            res = requests.get(ex_url, timeout=5).json()
            base_rate = res['rates']['KRW']
        except:
            base_rate = 1350.0

        # 2. 업비트 & 바이낸스 가격 가져오기
        upbit_btc = requests.get("https://api.upbit.com/v1/ticker?markets=KRW-BTC", timeout=5).json()[0]['trade_price']
        binance_btc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()['price']
        binance_krw = float(binance_btc) * base_rate

        # 3. 김치 프리미엄 계산
        kimp = ((upbit_btc / binance_krw) - 1) * 100

        # 4. 비트코인 도미넌스 가져오기 (CoinPaprika)
        global_url = "https://api.coinpaprika.com/v1/global"
        dom_res = requests.get(global_url, timeout=5).json()
        btc_dominance = dom_res['bitcoin_dominance_percentage']

        # 5. 공포 탐욕 지수 가져오기 (Alternative.me)
        # 0에 가까울수록 공포(Fear), 100에 가까울수록 탐욕(Greed)입니다.
        fgi_url = "https://api.alternative.me/fng/"
        fgi_res = requests.get(fgi_url, timeout=5).json()
        fgi_value = fgi_res['data'][0]['value']
        fgi_label = fgi_res['data'][0]['value_classification']

        # 6. 결과 출력 (원고의 감동을 실현!)
        print(f"✅ 비트코인 도미넌스: {btc_dominance:.2f}%")
        print(f"✅ 공포 탐욕 지수: {fgi_value} ({fgi_label})") # 원고 속 그 지수!
        print(f"✅ 김치 프리미엄: {kimp:.2f}%")
        print(f"✅ 적용 환율: {base_rate:,.2f} KRW/USD")
        print("-" * 40)

        # 7. 행동 강령 신호등
        if kimp > 5:
            print("🚨 신호등: [빨간불] 과열 구간! 매수 금지, 소고기 사드세요.")
        elif kimp > 2:
            print("⚠️ 신호등: [노란불] 관망 구간! 조급함을 버리세요.")
        else:
            print("🍏 신호등: [초록불] 매수 적기! 항공모함에 도토리를 채우세요.")
        print("-" * 40)

    except Exception as e:
        print(f"네오: 사령관님! 예상치 못한 성장통 발생! ㅋㅋㅋ\n에러 내용: {e}")

if __name__ == "__main__":
    get_market_data()
