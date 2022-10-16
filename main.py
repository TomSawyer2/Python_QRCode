import os
import sys
import getopt
from qrcode.encode.main import QRCode
from qrcode.decode.main import decodeQRCode


def decode(options):

    data = None

    for opt, arg in options:
        if opt in ('-d', '--data'):
            data = arg
    
    if data == None:
        print("请输入数据")
        return
    else:
        res = decodeQRCode(data.split(','))
        # "qrcode/assets/input.png"
        print('解码完成')
        print(res)


def encode(options):
    type = 'text'  # text file
    data = None
    output = 'terminal'  # terminal file
    filename = None
    outputdir = None

    qr = QRCode(None, 1)

    for opt, arg in options:
        if opt in ('-t', '--type'):
            type = arg
        elif opt in ('-d', '--data'):
            data = arg
        elif opt in ('-o', '--output'):
            output = arg
        elif opt in ('-f', '--filename'):
            filename = arg
        elif opt in '--outputdir':
            outputdir = arg

    if data is None:
        print("请输入数据")
        return

    if type == "text":
        qr.addData(data)
    elif type == "file":
        filePath = data
        # 从data对应的文件读取数据
        if os.path.exists(filePath):
            with open(filePath, 'r', encoding='utf-8') as f:
                data = f.read()
                qr.addData(data)

    if output == 'terminal':
        qr.printAscii()
    elif output == 'file':
        # 判断outputdir是否存在
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)

        qr.makeImage(filename, outputdir)

    print('编码成功')


def main(argv):
    args = getopt.getopt(argv, "d:t:o:f:", [
                         "encode", "decode", "data=", "type=", "output=", "filename=", "outputdir="])
    options = args[0]
    if options[0][0] == "--encode":
        encode(options)
    elif options[0][0] == "--decode":
        decode(options)
    else:
        print("请选择模式")


if __name__ == "__main__":
    main(sys.argv[1:])
