import json
from json import JSONDecodeError
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from requests import RequestException


def get_page_index():
    data={
        'type': '11',
        'interval_id': '100:90',
        'action':'',
        'start':'0',
        'limit': '20'
    }
    url='https://movie.douban.com/j/chart/top_list?'+ urlencode(data)
    print('索引页URL',url)
    # 此处是把字典对象转化为url的请求参数，此处不需要手动填写
    response = requests.get(url)
    try:
        if response.status_code == 200:
            return response.text
        return  None
    except RequestException:
        print('请求索引页出错')
        return None


def parse_page_index(html):
    try:
        data =json.loads(html)
        if data:
            #这边的data是list，但是其中的子项是dict
            for item in data:
                url = item.get('url')
                print('正在搜集电影链接',url)
                yield url
                #yield产生的是可迭代的对象，需要用循环提取其中的数据
        return None
    except JSONDecodeError:
        print('无法解析索引页',html)
        pass

def get_page_detail(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    try:
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错')
        return None

def parse_detail_page(html,url):
    soup = BeautifulSoup(html, 'lxml')
    ti


def main():
    html=get_page_index()
    for url in  parse_page_index(html):
        html = get_page_detail(url)



if __name__ == '__main__':
    main()


