import requests

def get_market_data():
    try:
        print("-" * 40)
        print(f"🚀 [시스템 사령관 코코의 마켓 센티넬 가동]")
        print("-" * 40)

        # 1. 환율 가져오기 (더 안정적인 오픈 API 사용)
        # 만약 특정 API가 막혀도 에러 없이 넘어가도록 예외처리를 강화했습니다.
        try:
            ex_url = "https://api.exchangerate-api.com/v4/latest/USD"
            res = requests.get(ex_url, timeout=5).json()
            base_rate = res['rates']['KRW']
        except:
            base_rate = 1350.0  # 혹시 모를 네트워크 오류 시 기본값 설정 (수동 수정 가능)

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

        # 5. 결과 출력
        print(f"✅ 비트코인 도미넌스: {btc_dominance:.2f}%")
        print(f"✅ 김치 프리미엄: {kimp:.2f}%")
        print(f"✅ 적용 환율: {base_rate:,.2f} KRW/USD")
        print("-" * 40)

        # 6. 행동 강령 신호등
        if kimp > 5:
            print("🚨 신호등: [빨간불] 과열 구간! 매수 금지, 소고기 사드세요.")
        elif kimp > 2:
            print("⚠️ 신호등: [노란불] 관망 구간! 조급함을 버리세요.")
        else:
            print("🍏 신호등: [초록불] 매수 적기! 항공모함에 도토리를 채우세요.")
        print("-" * 40)

    except requests.exceptions.ConnectionError:
        print("네오: 사령관님! 지금 인터넷 연결이 불안정하거나 주소에 접근이 안 됩니다!")
        print("와이파이를 확인하시거나 잠시 후 다시 실행해 주세요! ㅋㅋㅋ")
    except Exception as e:
        print(f"네오: 예상치 못한 성장통 발생! ㅋㅋㅋ\n에러 내용: {e}")

if __name__ == "__main__":
    get_market_data()
