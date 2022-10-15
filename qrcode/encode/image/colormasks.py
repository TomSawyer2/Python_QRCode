from __future__ import absolute_import

import math

from depcheck import Image


class QRColorMask:

    back_color = (255, 255, 255)
    has_transparency = False
    paint_color = back_color

    def initialize(self, styledPilImage, image):
        self.paint_color = styledPilImage.paint_color

    def apply_mask(self, image):
        width, height = image.size
        for x in range(width):
            for y in range(height):
                norm = self.extrap_color(
                    self.back_color, self.paint_color, image.getpixel((x, y))
                )
                if norm is not None:
                    image.putpixel(
                        (x, y),
                        self.interp_color(
                            self.get_bg_pixel(image, x, y),
                            self.get_fg_pixel(image, x, y),
                            norm,
                        ),
                    )
                else:
                    image.putpixel((x, y), self.get_bg_pixel(image, x, y))

    def get_fg_pixel(self, image, x, y):
        raise NotImplementedError("QRModuleDrawer.paint_fg_pixel")

    def get_bg_pixel(self, image, x, y):
        return self.back_color

    def interp_num(self, n1, n2, norm):
        return int(n2 * norm + n1 * (1 - norm))

    def interp_color(self, col1, col2, norm):
        return tuple(self.interp_num(col1[i], col2[i], norm) for i in range(len(col1)))

    def extrap_num(self, n1, n2, interped_num):
        if n2 == n1:
            return None
        else:
            return (interped_num - n1) / (n2 - n1)

    def extrap_color(self, col1, col2, interped_color):
        normed = []
        for c1, c2, ci in zip(col1, col2, interped_color):
            extrap = self.extrap_num(c1, c2, ci)
            if extrap is not None:
                normed.append(extrap)
        if not normed:
            return None
        return sum(normed) / len(normed)


class SolidFillColorMask(QRColorMask):

    def __init__(self, back_color=(255, 255, 255), front_color=(0, 0, 0)):
        self.back_color = back_color
        self.front_color = front_color
        self.has_transparency = len(self.back_color) == 4

    def apply_mask(self, image):
        if self.back_color == (255, 255, 255) and self.front_color == (0, 0, 0):
            pass
        else:
            QRColorMask.apply_mask(self, image)

    def get_fg_pixel(self, image, x, y):
        return self.front_color
