import requests
from bs4 import BeautifulSoup
import re
import os
import glob
from os import path
from aip import AipOcr
from PIL import Image
import time
import random
import json
import csv

from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

"""
1、本项目是保存公众号文章中的表情包，并识别表情包中文字当成名称命名。

2、抓包工具charles或者fiddler复制Header相关信息（失效后需要重新抓取）替换掉我的，params中去掉offset和count

3、替换百度aip接口中的三个参数，换成你自己的

4、运行代码

5、 本项目视频首发 B 站(菜鸟程序员的日常)
    文案首发公众号：Python知识圈（id：PythonCircle），欢迎关注，三连！
    视频链接：https://www.bilibili.com/video/BV1Vz41187Rt
    公众号文章链接：https://mp.weixin.qq.com/s/fVDwNdVDZo_0q6jAMWCGAA
"""

def request_data():
    article_url_list = []
    print('正在获取所有文章链接，请稍后')
    for offset in range(0, 323, 10):
        # 记得把offset后面的值改成{}
        base_url = 'http://mp.weixin.qq.com/mp/profile_ext?offset={}&count=10'
        # 下面的值以自己的为准，部分省略了

        cookies = {
            'wxuin': 'xxx',
            'devicetype': 'xxx-28',
            'version': 'xx',
            'lang': 'zh_CN',
            'rewardsn': '',
            'wxtokenkey': '777',
            'pass_ticket': 'x/x//x+x',
            'wap_sid2': 'xxxxx',
        }

        headers = {
            'Host': 'mp.weixin.qq.com',
            'user-agent': 'x/5.0 (Linux; x 9; STF-AL10 Build/HUAWEISTF-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1178 MMWEBSDK/180801 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/toolsmp',
            'x-requested-with': 'x',
            'accept': '*/*',
            'referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&x=x==&scen607xxx',
            'accept-language': 'zh-CN,en-US;q=0.9',
        }
        # 复制过来之后记得把offset和count去掉，offset值是动态的
        # 复制过来之后记得把offset和count去掉，offset值是动态的
        # 复制过来之后记得把offset和count去掉，offset值是动态的
        params = (
            ('action', 'getmsg'),
            ('__biz', 'xxxxxx=='),
            ('f', ['json', 'json']),
            ('is_ok', '1'),
            ('scene', '126'),
            ('uin', 'xxx'),
            ('key', 'xxx'),
            ('pass_ticket', 'zILyKILRyRlW0V/xxxx//xxx+5uNjV5AX'),
            ('wxtoken', ''),
            ('appmsg_token', 'xxxxxx~~'),
            ('x5', '0'),
        )
        # 代理ip，报pxory错误的话可能失效了，失效的话去西刺网自行更换，也可以直接去掉
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
        except Exception as e:
            time.sleep(2)
            print('获取文章链接失败', e)
        time.sleep(int(format(random.randint(2, 5))))
    return article_url_list


def baiduOCR(picfile):
    """利用百度api识别文本，并保存提取的文字
    picfile:    图片文件名
    """

    APP_ID = '填你自己注册应用的APP_ID'  # 刚才获取的ID，下同
    API_KEY = '填你自己注册应用的API_KEY'
    SECRECT_KEY = '填你自己注册应用的SECRECT_KEY'
    client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)
    i = open(picfile, 'rb')
    img = i.read()
    try:
        message = client.basicGeneral(img)['words_result']   # 通用文字识别，每天50000次免费
        # message = client.basicAccurate(img)   # 通用文字高精度识别，每天 800 次免费
        value = []
        for j in message:
            value.append(j['words'])
        t = ''.join(value)
        title = t.replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('<', '')\
            .replace('>', '').replace('|', '').replace('.', '')
        # .strip('/').strip('\\').strip(':').strip('*').strip('?').strip('<').strip('>').strip('|').strip('.')
        timestamp = int(time.time())
        if title == "" or title == None:
            title = timestamp
            return title
        i.close()
        return title
    except Exception as e:
        print(e)
        # print('此图片类型无法识别')


def get_urls(url):
    try:
        html = requests.get(url, timeout=30).text
    except requests.exceptions.SSLError:
        html = requests.get(url, verify=False, timeout=30).text
    except TimeoutError:
        print('请求超时')
    except Exception:
        print('获取图片链接失败')
    src = re.compile(r'data-src="(.*?)"')
    urls = re.findall(src, html)
    if urls is not None:
        url_list = []
        for url in urls:
            url_list.append(url)
        return url_list


def mkdir(base_path):
    isExists = os.path.exists(base_path)
    if not isExists:
        print('创建目录')
        os.makedirs(base_path)  # 创建目录
        os.chdir(base_path)  # 切换到创建的文件夹
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
        print('下载失败！！没有找到对应图片目前，请检查路径：', filename)
        pass
    except TimeoutError:
        print('下载超时：', filename)
        pass
    except Exception:
        print('非正常图片，直接忽略：', filename)
        pass


if __name__ == '__main__':
    for url in request_data():
        for url in urls:
            url_list = get_urls(url)
            base_path = r'./banfo/'
            mkdir(base_path)
            for pic_url in url_list:
                filename = base_path + \
                    pic_url.split('/')[-2] + '.' + pic_url.split('=')[-1]  # 图片的路径
                download(filename, pic_url)
                try:
                    title = baiduOCR(filename)
                    timestamp = int(time.time())
                    pic_type = pic_url.split('=')[-1]
                    if pic_type == 'gif':
                        new_name = base_path + str(timestamp) + '.' + pic_type
                    else:
                        new_name = base_path + str(title) + '.' + pic_type
                    os.rename(filename, new_name)
                    print('文件重命名成功% s' % (new_name))
                except Exception as e:
                    print('重命名失败！忽略')
