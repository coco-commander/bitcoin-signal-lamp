import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import datetime, timedelta
import warnings

# 1. 모든 워닝 차단 (빨간 글씨 안녕!)
warnings.filterwarnings("ignore")

# 2. 가장 안전한 한글 폰트 설정 (에러 원인 제거)
plt.rcParams['font.family'] = 'Malgun Gothic' # 윈도우 표준 폰트
plt.rcParams['axes.unicode_minus'] = False     # 마이너스 기호 깨짐 방지

def draw_v15_2_final():
    print("🚀 사령관님, 에러를 완전히 박멸한 '무결점 V15.2'를 실행합니다!")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=6*365)
    
    try:
        # 데이터 수집
        tickers = ["BTC-USD", "ETH-USD", "ADA-USD"]
        data = yf.download(tickers, start=start_date, end=end_date, progress=False)['Close']
        
        current_prices = data.iloc[-1]
        norm_data = (data / current_prices) * 100

        # 차트 그리기
        fig, ax = plt.subplots(figsize=(16, 9))

        # 고급진 색상 팔레트 (V15 프리미엄 유지)
        ax.plot(norm_data.index, norm_data['BTC-USD'], color='#b58900', lw=5, label='비트코인 (항공모함)', zorder=5)
        ax.plot(norm_data.index, norm_data['ETH-USD'], color='#073642', lw=3, label='이더리움 (대형함)', zorder=4)
        ax.plot(norm_data.index, norm_data['ADA-USD'], color='#859900', lw=2, label='에이다 (뗏목)', zorder=3)

        # 기준선 및 텍스트 (5년 전 정확 조준)
        ax.axhline(100, color='#262626', lw=2.5, zorder=6)
        ax.text(norm_data.index[100], 104, '현재 가격 (100%)', color='#262626', fontweight='bold', fontsize=12)

        two_years_ago = end_date - timedelta(days=2*365)
        ax.axvline(two_years_ago, color='#b58900', ls=':', lw=2, alpha=0.8)
       # ax.text(two_years_ago, 90, '비트코인: 고작 2년 전 가격', color='#b58900', fontweight='bold', ha='center', fontsize=11)

        five_years_ago = end_date - timedelta(days=5*365)
        ax.axvline(five_years_ago, color='#073642', ls=':', lw=2, alpha=0.8)
       # ax.text(five_years_ago, 70, '이더리움: 무려 5년 전 가격 (태초마을)', color='#073642', fontweight='bold', ha='center', fontsize=11)

        # 제목 및 라벨 (한글 깨짐 방지 최적화)
        ax.set_title("코린이 필독: 폭락장에서도 당신의 시간을 지켜주는 '항공모함'을 타라\n(현재 가격 대비 과거 가격 비율)", 
                     fontsize=20, fontweight='bold', pad=30)
        ax.set_ylabel("가격 비율 (현재=100%)", fontsize=14)
        ax.set_ylim(0, 380)
        ax.yaxis.set_major_formatter(mticker.PercentFormatter())
        ax.grid(True, axis='both', color='#e0e0e0', linestyle='-', lw=0.5)
        ax.legend(loc='upper right', fontsize=13, frameon=True, shadow=True, facecolor='white')

        plt.xticks(rotation=30, fontsize=12)
        plt.tight_layout()
        
        print(f"✅ 성공! 사령관님, 이제 예쁜 차트 보실 일만 남았습니다! ㅋㅋㅋ")
        plt.show()

    except Exception as e:
        print(f"네오가 이번엔 진짜 에러를 다 잡았는데... 혹시 또? : {e}")

if __name__ == "__main__":
    draw_v15_2_final()
