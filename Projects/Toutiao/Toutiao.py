from urllib.parse import urlencode
from requests.exceptions import RequestException
import requests
import json
from bs4 import BeautifulSoup
import re
import pymongo
from hashlib import md5
import os
from config import *
from multiprocessing import Pool
from json.decoder import JSONDecodeError

client = pymongo.MongoClient(MONGO_URL,connect=False)
db = client[MONGO_DB]


def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 3
    }
    url = 'https://www.toutiao.com/search_content/?'+ urlencode(data)
    print(url)
    #此处是把字典对象转化为url的请求参数，此处不需要手动填写
    response = requests.get(url)
    try:
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None

def parse_page_index(html):
    try:
        data = json.loads(html)
        #json.dump可以把数据转换成jsom格式，json.load将json文件转换为python类型的数据
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass

def get_page_detail(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    try:
        response= requests.get(url,headers=headers)
        if response.status_code ==200:
            return response.text
        return None
    except RequestException:
        print('请求详情出错', url)
        return None

def parse_page_detail(html,url):
    soup = BeautifulSoup(html, 'lxml')
    title =soup.select('title')[0].get_text()
    print(title)
    image_pattern= re.compile('var gallery =(.*?);', re.S)
    result =re.search(image_pattern,html)
    if result:
        data = json.loads(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images =data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:
                download_image(image)
            return {
                'title': title,
                'url': url,
                'images': images
            }

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('储存到MongoDB成功', result)
        return True
    return False

def download_image(url):
    print('正在下载', url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            save_image(response.content)
            return response.text
        return None
    except RequestException:
        print('请求图片出错', url)
        return None

def save_image(content):
    file_path ='{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()

def main(offset):
    html = get_page_index(offset, KEYWORD)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html,url)
            if result:
                save_to_mongo(result)

if __name__ == '__main__':
    groups = [x*20 for x in range(GROUP_START,GROUP_END)]
    pool=Pool()
    pool.map(main,groups)