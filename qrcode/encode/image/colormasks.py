from __future__ import absolute_import


class QRColorMask:

    backColor = (255, 255, 255)
    has_transparency = False
    paintColor = backColor

    def initialize(self, styledPilImage, image):
        self.paintColor = styledPilImage.paintColor

    def applyMask(self, image):
        width, height = image.size
        for x in range(width):
            for y in range(height):
                norm = self.extrapColor(
                    self.backColor, self.paintColor, image.getpixel((x, y))
                )
                if norm is not None:
                    image.putpixel(
                        (x, y),
                        self.interpColor(
                            self.getBgPixel(image, x, y),
                            self.getFgPixel(image, x, y),
                            norm,
                        ),
                    )
                else:
                    image.putpixel((x, y), self.getBgPixel(image, x, y))

    def getFgPixel(self, image, x, y):
        raise NotImplementedError("QRModuleDrawer.paint_fg_pixel")

    def getBgPixel(self, image, x, y):
        return self.backColor

    def interpNum(self, n1, n2, norm):
        return int(n2 * norm + n1 * (1 - norm))

    def interpColor(self, col1, col2, norm):
        return tuple(self.interpNum(col1[i], col2[i], norm) for i in range(len(col1)))

    def extrapNum(self, n1, n2, interped_num):
        if n2 == n1:
            return None
        else:
            return (interped_num - n1) / (n2 - n1)

    def extrapColor(self, col1, col2, interped_color):
        normed = []
        for c1, c2, ci in zip(col1, col2, interped_color):
            extrap = self.extrapNum(c1, c2, ci)
            if extrap is not None:
                normed.append(extrap)
        if not normed:
            return None
        return sum(normed) / len(normed)


class SolidFillColorMask(QRColorMask):

    def __init__(self, backColor=(255, 255, 255), frontColor=(0, 0, 0)):
        self.backColor = backColor
        self.frontColor = frontColor
        self.has_transparency = len(self.backColor) == 4

    def applyMask(self, image):
        if self.backColor == (255, 255, 255) and self.frontColor == (0, 0, 0):
            pass
        else:
            QRColorMask.applyMask(self, image)

    def getFgPixel(self, image, x, y):
        return self.frontColor
