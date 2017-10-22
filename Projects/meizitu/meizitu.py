import requests
from requests.exceptions import RequestException
import re

def get_page_index():
    url='http://www.mzitu.com/taiwan/page/2/'
    response= requests.get(url)
    try:
        if response.status_code ==200:
            print(response.text)
        return None
    except RequestException:
        print('请求页面出错')
        return None

def parse_page_index(html):
    pattern= re.compile('<li><a href="(.*?)" target="_blank">',re.S)
    result= re.search(pattern, html)
    if result:
        link =result.group(1)
        for li in link:
            print(li)

def main():
    html= get_page_index()
    print(html)

if __name__ == '__main__':
    main()


