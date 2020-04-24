import glob
from os import path
import os
from aip import AipOcr
from PIL import Image
import time


"""
1、本项目是根据图片或者表情包中文字重命名你的图片或者表情包，不支持gif图片。

2、替换百度aip接口中的三个参数，换成你自己的

3、把pic_path的路径替换成你需要重命名的图片的文件夹路径，路径后不要少了/，否则就不是文件夹了

4、运行代码

5、 本项目视频首发 B 站(菜鸟程序员的日常)
    文案首发公众号：Python知识圈（id：PythonCircle），欢迎关注，三连！
    视频链接：https://www.bilibili.com/video/BV1Vz41187Rt
    公众号文章链接：https://mp.weixin.qq.com/s/fVDwNdVDZo_0q6jAMWCGAA
"""

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
        title = ''.join(value)
        timestamp = int(time.time())
        if title == "":
            title = timestamp
            return title
        i.close()
        return title
    except Exception:
        pass
        # print('此图片类型无法识别')


pic_path = r'/Users/brucepk/Pictures/banfo/'   # 目标路径，需要改成你自己需要改名称的路径，最后最后的/不要漏了

"""os.listdir(path) 操作效果为 返回指定路径(path)文件夹中所有文件名"""

filename_list = os.listdir(pic_path)  # 扫描目标路径的文件,将文件名存入列表

a = 0
for i in filename_list:
    try:
        used_name = pic_path + filename_list[a]
        title = baiduOCR(used_name)
        timestamp = int(time.time())
        pic_type = i.split('.')[-1]
        if pic_type == 'gif':
            new_name = pic_path + str(timestamp) + '.' + i.split('.')[-1]
        else:
            new_name = pic_path + str(title) + '.' + i.split('.')[-1]
        os.rename(used_name, new_name)
        print('文件重命名成功,新的文件名为 % s' % (new_name))
    except Exception:
        pass
    a += 1
