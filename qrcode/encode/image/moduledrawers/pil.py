from qrcode.encode.image.depcheck import ImageDraw
from qrcode.encode.image.moduledrawers.base import QRModuleDrawer

ANTIALIASING_FACTOR = 4


class SquareModuleDrawer(QRModuleDrawer):

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self.imgDraw = ImageDraw.Draw(self.img._img)

    def drawrect(self, box, isActive: bool):
        if isActive:
            self.imgDraw.rectangle(box, fill=self.img.paintColor)
