import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

import requests
import lxml.html

import os
from pyquery import PyQuery as pq
from config import *
import re

browser = webdriver.Chrome(service_args=SERVICE_ARGS)
browser.set_window_size(1400,900)

wait = WebDriverWait(browser, 10)

def parser(url, param):
    browser.get(url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, param)))
    html = browser.page_source
    doc = pq(html)
    return doc

def get_main_url():
    print('打开主页搜寻链接中...')
    try:
        doc = parser('https://huaban.com/boards/favorite/funny/', '#waterfall')
        items = doc('#waterfall').items()
        id_pattern= re.search('')
        for item in items:
            print(item[0])
        # for item in items:
        #     id = item.find('.data-seq').text()
        #     print(id)
        #     main_url = 'https://huaban.com/boards/' + item
        #     print('主链接已找到' + main_url)
        #     fileName = item.find('.over').text()
        #     print(fileName)
        #     if '*' in fileName:
        #         fileName = fileName.replace('*', '')
            #download(main_url, fileName)
    except Exception as e:
        print(e)

def download(main_url, fileName):
    print('-------准备下载中-------')
    try:
        doc = parser(main_url, '#waterfall')
        if not os.path.exists('image\\' + fileName):
            print('创建文件夹...')
            os.makedirs('image\\' + fileName)
        link = doc.xpath('//*[@id="waterfall"]/div/a/@href')
        # print(link)
        i = 0
        for item in link:
            i += 1
            minor_url = 'http://huaban.com' + item
            doc = parser(minor_url, '#pin_view_page')
            img_url = doc.xpath('//*[@id="baidu_image_holder"]/a/img/@src')
            img_url2 = doc.xpath('//*[@id="baidu_image_holder"]/img/@src')
            img_url +=img_url2
            try:
                url = 'http:' + str(img_url[0])
                print('正在下载第' + str(i) + '张图片，地址：' + url)
                r = requests.get(url)
                filename = 'image\\{}\\'.format(fileName) + str(i) + '.jpg'
                with open(filename, 'wb') as fo:
                    fo.write(r.content)
            except Exception:
                print('出错了！')
    except Exception:
        print('出错啦!')




def main():
    get_main_url()


if __name__ == '__main__':
    main()
