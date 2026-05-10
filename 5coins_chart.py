import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import datetime, timedelta
import warnings

# 1. 모든 워닝 차단
warnings.filterwarnings("ignore")

# 2. 폰트 설정 (클라우드 환경에 맞춰 한글 폰트 주석 처리 유지)
plt.rcParams['axes.unicode_minus'] = False

def draw_v15_3_pentagon():
    print("🚀 사령관님, '5대 핵심 자산(BTC/SOL/RENDER/SUI/ONDO)' 정밀 분석 작전을 시작합니다!")
    
    end_date = datetime.now()
    # 신생 코인들을 위해 데이터 수집 기간을 넉넉히 잡되, 데이터가 있는 시점부터 그려집니다.
    start_date = end_date - timedelta(days=5*365)
    
    try:
        # 데이터 수집 (사령관님의 타겟 5종)
        tickers = ["BTC-USD", "SOL-USD", "RENDER-USD", "SUI-USD", "ONDO-USD"]
        data = yf.download(tickers, start=start_date, end=end_date, progress=False)['Close']
        
        # 현재 가격 기준으로 정규화 (현재=100%)
        current_prices = data.iloc[-1]
        norm_data = (data / current_prices) * 100

        # 차트 그리기
        fig, ax = plt.subplots(figsize=(16, 9))

        # 5대 천왕 색상 팔레트 (강렬하고 구분 잘 되는 색상들)
        ax.plot(norm_data.index, norm_data['BTC-USD'], color='#b58900', lw=5, label='Bitcoin (항공모함)', zorder=10)
        ax.plot(norm_data.index, norm_data['SOL-USD'], color='#073642', lw=3, label='Solana (쾌속정)', zorder=9)
        ax.plot(norm_data.index, norm_data['RENDER-USD'], color='#cb4b16', lw=2, label='Render (AI 엔진)', zorder=8)
        ax.plot(norm_data.index, norm_data['SUI-USD'], color='#268bd2', lw=2, label='Sui (신형 구축함)', zorder=7)
        ax.plot(norm_data.index, norm_data['ONDO-USD'], color='#d33682', lw=2, label='Ondo (RWA 선단)', zorder=6)

        # 현재 가격 기준선 (100%)
        ax.axhline(100, color='#262626', lw=2.5, ls='--', alpha=0.5, zorder=5)
        ax.text(norm_data.index[0], 105, '현재 가격 (100%)', color='#262626', fontweight='bold')

        # 제목 및 스타일 (영문으로 작성하여 폰트 깨짐 방지)
        ax.set_title("Strategy V15.3: Core 5 Assets Relative Value Analysis\n(Current Price = 100%)", 
                     fontsize=20, fontweight='bold', pad=30)
        ax.set_ylabel("Price Ratio (%)", fontsize=14)
        
        # Y축 범위 조정 (코인들의 변동폭에 따라 자동 조절되도록 설정)
        ax.yaxis.set_major_formatter(mticker.PercentFormatter())
        ax.grid(True, axis='both', color='#e0e0e0', linestyle='-', lw=0.5)
        ax.legend(loc='upper left', fontsize=12, frameon=True, shadow=True)

        plt.xticks(rotation=30, fontsize=12)
        plt.tight_layout()
        
        # 파일 저장
        output_name = 'pentagon_chart.png'
        plt.savefig(output_name)
        print(f"✅ 작전 성공! 사령관님, '{output_name}' 파일이 생성되었습니다! ㅋㅋㅋ")

    except Exception as e:
        print(f"네오 긴급 보고! 데이터 수집 중 교전 발생 : {e}")

if __name__ == "__main__":
    draw_v15_3_pentagon()
