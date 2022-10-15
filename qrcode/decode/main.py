import os
import sys
import requests
from io import BytesIO
from pyzbar import pyzbar
from PIL import Image


def decodeQRCode(imageUrls):
    """
    通过图片地址获取二维码信息
    :param imageUrls: list 图片地址数组
    :return: list 二维码信息数组，顺序与图片地址数组一致
    """

    # 类似JS中Promise.all的实现
    imageUrlsLen = len(imageUrls)
    resList = [''] * imageUrlsLen
    resolvedCnt = 0

    for i, imageUrl in enumerate(imageUrls):
        if os.path.isfile(imageUrl):
            img = Image.open(imageUrl)
        else:
            reqImg = requests.get(imageUrl).content
            img = Image.open(BytesIO(reqImg))

        textList = pyzbar.decode(img)

        for text in textList:
            data = text.data.decode("utf-8")
            resList[i] = data
            resolvedCnt += 1
            if (resolvedCnt == imageUrlsLen):
                return resList


# 解析本地二维码
# get_ewm(r'qrcode\assets\input.png')

if __name__ == '__main__':
    imageUrls = sys.argv[1:]
    info = decodeQRCode(imageUrls)
    print(info)
