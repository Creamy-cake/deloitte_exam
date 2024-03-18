import json

import pandas as pd
import numpy as np
import re
import requests
import base64
# 图片识别
from aip import AipOcr
# 时间模块
import time
# 网页获取
import requests
# 操作系统接口模块
import os

def ocr_1(img_path: str) -> list:

    #根据图片路径，将图片转为文字，返回识别到的字符串列表

    # 请求头
    headers = {
        'Host': 'cloud.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.76',
        'Accept': '*/*',
        'Origin': 'https://cloud.baidu.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://cloud.baidu.com/product/ocr/general',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }
    # 打开图片并对其使用 base64 编码
    with open(img_path, 'rb') as f:
        img = base64.b64encode(f.read())
    data = {
        'image': 'data:image/jpeg;base64,'+str(img)[2:-1],
        'image_url': '',
        'type': 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic',
        'detect_direction': 'false'
    }
    # 开始调用 ocr 的 api
    response = requests.post(
        'https://cloud.baidu.com/aidemo', headers=headers, data=data)

    # 设置一个空的列表，后面用来存储识别到的字符串
    ocr_text = []
    result = response.json()['data']
    #if not result.get('words_result'):
        #return []

    num = 0

    print(type(result))

    if type(result) is not dict:
        result = eval(result)

    for item in result['words_result']:
        if num == 0:
            ocr_title = list(item.values())[0]
        elif "单位" in list(item.values())[0]:
            ocr_unit = list(item.values())[0]
            break
        num += 1

    return ocr_title, ocr_unit

# 获取文件夹中所有图片
def get_image(image_path):
    images = []  # 存储文件夹内所有文件的路径（包括子目录内的文件）
    for root, dirs, files in os.walk(image_path):
        path = [os.path.join(root, name) for name in files]
        images.extend(path)
        print(path)
    return images

def Image_Excel(APP_ID, API_KEY, SECRET_KEY,image_path):
    #  调用百度AI接口
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # 循环遍历文件家中图片
    images = get_image(image_path)
    for image in images:
        # 以二进制方式打开图片
        img_open = open(image, 'rb')
        # 读取图片
        img_read = img_open.read()
        # 调用表格识别模块识别图片
        table = client.tableRecognitionAsync(img_read)
        # 获取请求ID
        request_id = table['result'][0]['request_id']
        # 获取表格处理结果
        result = client.getTableRecognitionResult(request_id)
        # 处理状态是“已完成”，获取下载地址
        while result['result']['ret_msg'] != '已完成':
            time.sleep(2)  # 暂停2秒再刷新
            result = client.getTableRecognitionResult(request_id)
        download_url = result['result']['result_data']
        print(download_url)
        # 获取表格数据
        excel_data = requests.get(download_url)
        # 根据图片名字命名表格名称
        xlsx_name = image.split(".")[0] + ".xls"
        # 新建excel文件
        xlsx = open(xlsx_name, 'wb')
        # 将数据写入excel文件并保存
        xlsx.write(excel_data.content)
        xlsx.close()
        df = pd.read_excel(xlsx_name,engine='xlrd')
        break
    return df

if __name__ == '__main__':
    img_path = "D:\code\ocr\ordinary\o_test.png"
    print(ocr_1(img_path))
    final_dict = {}
    ocr = ocr_1(img_path)
    final_dict['title'] = ocr[0]
    final_dict['unit'] = ocr[1]

    image_path = "D:\\code\\ocr\\ordinary"
    APP_ID = '56618439'
    API_KEY = 'GLfSnI9WMwqPai81QqeetpMj'
    SECRET_KEY = 'Co0yPRDbvlwf8nN7I6HtW0jNovIR5j4I'
    df = Image_Excel(APP_ID, API_KEY, SECRET_KEY,image_path)
    final_dict['header'] = list(df.head(0))
    final_dict['key_index'] = list(df.loc[ : ,"项目名称"])
    values = []
    data1 = list(df.loc[0])[1:]
    data2 = list(df.loc[1])[1:]
    data3 = list(df.loc[2])[1:]
    values.append(data1)
    values.append(data2)
    values.append(data3)
    final_dict['values'] = values
    print(final_dict)



