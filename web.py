# 此文件为Web服务的后端，不需要直接运行
import base64
import os
import time
from flask import Flask, request, send_file
from flask_cors import CORS
from qrcode.encode.main import QRCode
from qrcode.decode.main import decodeQRCode

app = Flask(__name__, static_folder='web/dist')

DIST_DIR = 'web\dist'


CORS(app, resources=r'/*')


def responseConstructor(code, message, data):
    # 标准的response格式
    return {
        "code": code,
        "message": message,
        "data": data
    }


@app.route('/')
def index_client():
    entry = os.path.join(DIST_DIR, 'index.html')
    return send_file(entry)


@app.route('/web/dist/<path:path>')
def static_proxy(path):
    # 静态文件代理
    entry = os.path.join(DIST_DIR, path)
    return send_file(entry)


@app.route("/api")
def index():
    return responseConstructor(0, "Hello World", None)


"""
POST /api/encode
:param: data 要编码的数据
"""


@app.route("/api/encode", methods=['POST'])
def decodeService():
    req = request.get_json()
    data = req.get("data")
    if data is None:
        return responseConstructor(1, "data is None", None)
    qr = QRCode(None, 1)
    qr.addData(data)
    now = int(time.time())
    fileName = 'output-' + str(now) + '.png'
    im = qr.makeImage(fileName, "", False)
    fileRoute = 'qrcode/assets/' + fileName
    im.save(fileRoute)
    with open(fileRoute, 'rb') as f:
        data = f.read()
        data = base64.b64encode(data).decode('utf-8')
        return responseConstructor(0, "解码成功", data)


"""
POST /api/decode
:param: data 要解码的数据（Base64）
"""


@app.route("/api/decode", methods=['POST'])
def encodeService():
    req = request.get_json()
    data = req.get("data")
    if data is None:
        return responseConstructor(1, "data is None", None)
    # 保存图片
    now = int(time.time())
    fileName = 'input-' + str(now) + '.png'
    fileRoute = 'qrcode/assets/' + fileName
    with open(fileRoute, 'wb') as f:
        f.write(base64.b64decode(data))
    # 解码
    res = decodeQRCode([fileRoute])
    return responseConstructor(0, "编码成功", res)


if __name__ == "__main__":
    app.run()
