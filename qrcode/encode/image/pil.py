import qrcode.encode.image.base
from qrcode.encode.image.depcheck import Image, ImageDraw


class PilImage(qrcode.encode.image.base.BaseImage):

    kind = "PNG"

    def newImage(self, **kwargs):
        backColor = kwargs.get("backColor", "white")
        fillColor = kwargs.get("fillColor", "black")

        try:
            fillColor = fillColor.lower()
        except AttributeError:
            pass

        try:
            backColor = backColor.lower()
        except AttributeError:
            pass

        if fillColor == "black" and backColor == "white":
            mode = "1"
            fillColor = 0
            backColor = 255
        elif backColor == "transparent":
            mode = "RGBA"
            backColor = None
        else:
            mode = "RGB"

        img = Image.new(mode, (self.pixelSize, self.pixelSize), backColor)
        self.fillColor = fillColor
        self._idr = ImageDraw.Draw(img)
        return img

    def drawrect(self, row, col):
        box = self.pixelBox(row, col)
        self._idr.rectangle(box, fill=self.fillColor)

    def save(self, stream, format=None, **kwargs):
        kind = kwargs.pop("kind", self.kind)
        if format is None:
            format = kind
        self._img.save(stream, format=format, **kwargs)

    def __getattr__(self, name):
        return getattr(self._img, name)
