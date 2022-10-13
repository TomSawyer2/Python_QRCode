import os
import requests
from io import BytesIO
from pyzbar import pyzbar
from PIL import Image


def get_ewm(img_adds):
    """ 读取二维码的内容： img_adds：二维码地址（可以是网址也可是本地地址 """
    if os.path.isfile(img_adds):
        # 从本地加载二维码图片
        img = Image.open(img_adds)
    else:
        # 从网络下载并加载二维码图片
        rq_img = requests.get(img_adds).content
        img = Image.open(BytesIO(rq_img))

    txt_list = pyzbar.decode(img)

    for txt in txt_list:
        barcodeData = txt.data.decode("utf-8")
        print(barcodeData)

# 解析本地二维码
get_ewm(r'qrcode\decode\test.png')