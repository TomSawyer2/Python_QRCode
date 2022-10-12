from main import QRCode

def main():
    qr = QRCode()
    qr.addData("Hello WorldHello WorldHello WororldHello WorldHellello WorldHello World")
    qr.print_ascii()

main()