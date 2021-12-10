import plotly
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import random
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests


#함수형태 변환
b = pd.DataFrame(index=range(0, 0), columns=["시간",
                                             "종목코드",
                                             "기업명",
                                             "현재가",
                                             "전일대비 상승하락",
                                             "전일대비",
                                             "전일대비%",
                                             "전일가",
                                             "시가",
                                             "고가",
                                             "상한가",
                                             "저가",
                                             "하한가",
                                             "거래량",
                                             "거래대금"])
def get_bs_obj(k):
    c=[]
    url = "https://finance.naver.com/item/main.nhn?code={}".format(k)
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")
    no_today = bs_obj.find("div", {"class":"new_totalinfo"})
    blind_now = no_today.find("dl", {"class":"blind"})
    a = blind_now.get_text().split("\n")
    c.extend([a[2],
              re.sub(r'.*\s([0-9]+)\s.*',r'\1',a[4]),
              a[3][4:],
              a[5].split("현재가 ")[1].split(" 전일대비 ")[0],
              re.sub(r'.*["전일대비"]\s(["가-힇"]+)\s.*',r'\1',a[5]),
              re.sub(r'.*["전일대비"]\s["가-힇"]+\s(.*)\s[가-힇]+\s.*',r'\1',a[5]),
              re.sub(r'.*["전일대비"]\s["가-힇"]+\s.*\s[가-힇]+\s(.*)\s["가-힇"]+',r'\1',a[5]),
              a[6][4:],
              a[7][3:],
              a[8][3:],
              a[9][4:],
              a[10][3:],
              a[11][4:],
              a[12][4:],
              a[13][5:]])
    b.loc[k] = c
# # #호출
# bs_obj = get_bs_obj()
# no_today = bs_obj.find("div", {"class":"new_totalinfo"})
# blind_now = no_today.find("dl", {"class":"blind"})
# a = blind_now.get_text().split("\n")

k_list = ["005930","035720","068270","036570","000660"]
for i in range(0,len(k_list)):
    get_bs_obj(k_list[i])
b = b.reset_index(drop=True)

for j in range(0,len(b["전일대비"])):
    if b["전일대비 상승하락"][j] == "보합":
        b["전일대비"][j] =0
        b["전일대비%"][j] =0.00
