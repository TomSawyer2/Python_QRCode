from qrcode.decode.main import decodeQRCode
from qrcode.encode.main import QRCode


def encodeTest():
    qr = QRCode(None, 1)
    qr.addData("666")
    qr.makeImage(backColor="red")
    qr.printAscii()

encodeTest()

def decodeTest():
    res = decodeQRCode(["qrcode/assets/input.png"])
    print(res)

decodeTest()
