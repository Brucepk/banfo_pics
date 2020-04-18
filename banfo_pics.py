import requests
import time
import json
import csv
import random
from bs4 import BeautifulSoup
import re
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


def request_data():
    article_url_list = []
    print('正在下载，请稍等！大约需要30分钟')
    for offset in range(0, 310, 10):
        # 记得把offset后面的值改成{}
        base_url = 'http://mp.weixin.qq.com/mp/profile_ext?offset={}&count=10'

        # 下面的值以自己的为准，部分省略了，从转换工具里复制过来就行
        # 下面的值以自己的为准，部分省略了，从转换工具里复制过来就行
        # 下面的值以自己的为准，部分省略了，从转换工具里复制过来就行

        cookies = {
            'devicetype': 'xxx',
            'lang': 'xx',
            'pass_ticket': 'xxxx',
            'version': '27000d37',
        }

        headers = {
            'Host': 'mp.weixin.qq.com',
            'Accept': '*/*',
            'User-Agent': 'xx',
            'Referer': 'xxx',
            'Accept-Language': 'zh-cn',
            'X-Requested-With': 'XMLHttpRequest',
        }

        params = (
            ('action', 'getmsg'),
            ('__biz', 'MzI5MTE2NDI2OQ=='),
            ('f', ['json', 'json']),
            ('is_ok', '1'),
            ('scene', '124'),
            ('uin', 'MjQ5NjQ5NjEzNg=='),
            ('key',
             'xxx'),
            ('pass_ticket', 'xxx'),
            ('wxtoken', ''),
            ('appmsg_token', 'xxx'),
            ('x5', '0'),
        )

        # 代理ip，失效的话请自行更换，也可以直接去掉
        proxy = {'https': '114.239.144.61:808'}

        try:
            response = requests.get(
                base_url.format(offset),
                headers=headers,
                params=params,
                cookies=cookies,
                proxies=proxy)
            if 200 == response.status_code:
                all_datas = json.loads(response.text)
                if 0 == all_datas['ret'] and all_datas['msg_count'] > 0:
                    summy_datas = all_datas['general_msg_list']
                    datas = json.loads(summy_datas)['list']
                    for data in datas:
                        try:
                            article_url = data['app_msg_ext_info']['content_url']
                            article_url_list.append(article_url)
                        except Exception as e:
                            continue
        except:
            time.sleep(2)
        time.sleep(int(format(random.randint(2, 5))))
    return article_url_list


def get_urls(url):
    try:
        html = requests.get(url, timeout=30).text
    except requests.exceptions.SSLError:
        html = requests.get(url, verify=False, timeout=30).text
    except TimeoutError:
        print('请求超时')
    except Exception:
        print('获取失败')
    src = re.compile(r'data-src="(.*?)"')
    urls = re.findall(src, html)
    if urls is not None:
        url_list = []
        for url in urls:
            url_list.append(url)
        return url_list


def mkdir():
    isExists = os.path.exists(r'./banfo')
    if not isExists:
        print('创建目录')
        os.makedirs(r'./banfo')  # 创建目录
        os.chdir(r'./banfo')  # 切换到创建的文件夹
        return True
    else:
        print('目录已存在，即将保存！')
        return False


def download(filename, url):
    try:
        with open(filename, 'wb+') as f:
            try:
                f.write(requests.get(url, timeout=30).content)
                print('成功下载图片：', filename)
            except requests.exceptions.SSLError:
                f.write(requests.get(url, verify=False, timeout=30).content)
                print('成功下载图片：', filename)
    except FileNotFoundError:
        print('下载失败，非表情包，直接忽略：', filename)
    except TimeoutError:
        print('下载超时：', filename)
    except Exception:
        print('下载失败：', filename)


if __name__ == '__main__':
    for url in request_data():
        url_list = get_urls(url)
        mkdir()
        for pic_url in url_list:
            filename = r'./banfo/' + pic_url.split('/')[-2] + '.' + pic_url.split('=')[-1]   # 图片的路径
            download(filename, pic_url)

