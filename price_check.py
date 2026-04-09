import requests
from datetime import datetime

# 비트코인 현재가 가져오기 (무료 API 사용)
url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
response = requests.get(url)
data = response.json()
price = data['bpi']['USD']['rate']

print(f"[{datetime.now()}] 현재 비트코인 가격: ${price}")

# 이 기록을 'history.txt' 파일에 저장하기
with open("history.txt", "a") as f:
    f.write(f"{datetime.now()}: ${price}\n")
