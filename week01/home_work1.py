# 使用BeautifulSoup解析网页

import requests
from bs4 import BeautifulSoup as bs
# bs4是第三方库需要使用pip命令安装

header = {
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
    'Accept': "*/*",
    'Accept-Encoding': 'gazip, deflate, br',
    'Accept-Language': 'en-AU,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,la;q=0.6',
    'Content-Type': 'text/plain',
    'Connection': 'keep-alive',
    # 'Host': 'wreport1.meituan.net',
    'Origin': 'https://maoyan.com',
    'Referer': 'https://maoyan.com/films?showType=3',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
}

myurl = 'https://maoyan.com/films?showType=3'

response = requests.get(myurl,headers=header)
bs_info = bs(response.text, 'html.parser')

mylist = []

ddtags = bs_info.find('dl', attrs={'class': 'movie-list'}).find_all('dd',limit=10)

for ddtag in ddtags:
    minfos = ddtag.find('div', attrs={'class': 'movie-hover-info'}).find_all('div', attrs={'class': 'movie-hover-title'})
    movie_name = minfos[0].find('span', attrs={'class': 'name'}).text
    movie_type = minfos[1].contents[2].strip()
    movie_time = minfos[3].contents[2].strip()
    # print("{}.电影名称：{} 电影类型：{} 上映时间：{}".format(movie_name, movie_type, movie_time))
    mylist.append([movie_name, movie_type, movie_time])

import pandas as pd

movie1 = pd.DataFrame(data = mylist)

movie1.to_csv('./home_work1.csv', encoding='utf8', index=False, header=False)