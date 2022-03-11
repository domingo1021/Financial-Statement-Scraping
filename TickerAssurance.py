# import pandas as pd
# import requests

# class Ticker:
#     def scrape_ticker():
#         res = requests.get("http://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
#         df = pd.read_html(res)

# def scrape_ticker():
#     res = requests.get("http://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
#     df = pd.read_html(res.text)[0]
#     return df

# print(scrape_ticker().iloc[:9000][0])