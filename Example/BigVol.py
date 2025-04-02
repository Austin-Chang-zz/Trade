import requests
import pandas as pd

# 抓取台股即時數據
url = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_t00.tw"
response = requests.get(url)
data = response.json()

# 解析成交量變化
stocks = []
for stock in data['msgArray']:
    stock_info = {
        "代號": stock['c'],
        "名稱": stock['n'],
        "成交量": int(stock['v']),
        "現價": float(stock['z']) if stock['z'] else None,
        "昨收": float(stock['y']) if stock['y'] else None
    }
    stocks.append(stock_info)

df = pd.DataFrame(stocks)
df['成交量倍數'] = df['成交量'] / df['昨收']
df = df.sort_values(by="成交量倍數", ascending=False)

print(df.head(15))  # 選出前15名當沖股
