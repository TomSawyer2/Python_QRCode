from __future__ import absolute_import


from qrcode.encode.image.depcheck import ImageDraw
from qrcode.encode.image.moduledrawers.base import QRModuleDrawer

ANTIALIASING_FACTOR = 4


class StyledPilQRModuleDrawer(QRModuleDrawer):
    img: "StyledPilImage"


class SquareModuleDrawer(StyledPilQRModuleDrawer):
    """
    正方形绘图
    """

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self.imgDraw = ImageDraw.Draw(self.img._img)

    def drawrect(self, box, is_active: bool):
        if is_active:
            self.imgDraw.rectangle(box, fill=self.img.paint_color)
