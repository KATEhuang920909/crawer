# -*- coding: utf-8 -*-
"""
 Time : 2020/8/24 21:34
 Author : huangkai
 File : jrj_crawer.py
 Software: PyCharm 
 mail:18707125049@163.com
 
"""
import datetime
from bs4 import BeautifulSoup
import requests
import re
from zhon.hanzi import punctuation
import string


def datetime_shift(y, m, d):  # 后一天
    y = int(y)
    m = int(m)
    d = int(d)
    date = datetime.date(y, m, d)
    date_ = date + datetime.timedelta(days=-1)
    month_str = str(date_.month)
    day_str = str(date_.day)
    if len(str(date_.month)) == 1:
        month_str = '0' + month_str
    if len(str(date_.day)) == 1:
        day_str = '0' + day_str
    return str(date_.year), month_str, day_str


def get_content_url_list(url):  # 某一天的新闻列表
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    content = soup.find_all(name='li')
    patter = re.compile('</em><a href="(.*?)">.*?')
    url_list = re.findall(patter, str(content))
    return url_list


def get_news(url):
    news = []
    for i in range(10):
        temp_news = []
        if i == 0:
            html = requests.get(url)

        else:
            url = url.split('.shtml')[0] + '-' + str(i) + '.shtml'
            html = requests.get(url)
        soup = BeautifulSoup(html.text)
        if i == 0:
            title = soup.find_all(name='title')  # 标题
        content = soup.find_all(name='p')
        for text in content:
            if text.text:
                if text.text[0] == '\u3000':
                    temp_news.append(text.text)
                else:
                    if temp_news != []:
                        break
        if temp_news != []:
            news += temp_news
        else:
            break

    if news != []:
        return news, title[0].string
    else:
        return '', ''


if __name__ == '__main__':
    year = '2020'
    month = '08'
    day = '22'
    i = 0
    while i < 20:
        url = 'http://insurance.jrj.com.cn/xwk/{}/{}_1.shtml'.format(year + month, year + month + day)
        url_list = get_content_url_list(url)
        print(url_list)
        for news_url in url_list:
            news, title = get_news(news_url)
            print(title)
            if news != '':
                temp_title=title
                for c in punctuation + string.punctuation:
                    temp_title = temp_title.replace(c, "")
                with open('data//' + temp_title + '.txt', 'w', encoding='utf-8') as f:
                    f.write(title + '\n')
                    for new in news:
                        f.write(new + '\n')
        year, month, day = datetime_shift(year, month, day)
        i += 1
