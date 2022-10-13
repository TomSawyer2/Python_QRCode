from main import QRCode

def main():
    qr = QRCode(None, 1)
    qr.addData("666")
    qr.printAscii()

main()