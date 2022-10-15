from __future__ import absolute_import

import qrcode.encode.image.base
from qrcode.encode.image.colormasks import QRColorMask, SolidFillColorMask
from qrcode.encode.image.depcheck import Image
from qrcode.encode.image.moduledrawers.pil import SquareModuleDrawer


class StyledPilImage(qrcode.encode.image.base.BaseImageWithDrawer):

    kind = "PNG"

    needs_processing = True
    color_mask: QRColorMask
    default_drawer_class = SquareModuleDrawer

    def __init__(self, *args, **kwargs):
        self.color_mask = kwargs.get("color_mask", SolidFillColorMask())
        embeded_image_path = kwargs.get("embeded_image_path", None)
        self.embeded_image = kwargs.get("embeded_image", None)
        self.embeded_image_resample = kwargs.get(
            "embeded_image_resample", Image.LANCZOS
        )
        if not self.embeded_image and embeded_image_path:
            self.embeded_image = Image.open(embeded_image_path)

        self.paint_color = tuple(0 for i in self.color_mask.back_color)
        if self.color_mask.has_transparency:
            self.paint_color = tuple([*self.color_mask.back_color[:3], 255])

        super().__init__(*args, **kwargs)

    def new_image(self, **kwargs):
        mode = (
            "RGBA"
            if (
                self.color_mask.has_transparency
                or (self.embeded_image and "A" in self.embeded_image.getbands())
            )
            else "RGB"
        )
        back_color = self.color_mask.back_color

        return Image.new(mode, (self.pixel_size, self.pixel_size), back_color)

    def init_new_image(self):
        self.color_mask.initialize(self, self._img)
        super().init_new_image()

    def process(self):
        self.color_mask.apply_mask(self._img)
        if self.embeded_image:
            self.draw_embeded_image()

    def draw_embeded_image(self):
        if not self.embeded_image:
            return
        total_width, _ = self._img.size
        total_width = int(total_width)
        logo_width_ish = int(total_width / 4)
        logo_offset = (
            int((int(total_width / 2) - int(logo_width_ish / 2)) / self.box_size)
            * self.box_size
        )
        logo_position = (logo_offset, logo_offset)
        logo_width = total_width - logo_offset * 2
        region = self.embeded_image
        region = region.resize((logo_width, logo_width), self.embeded_image_resample)
        if "A" in region.getbands():
            self._img.alpha_composite(region, logo_position)
        else:
            self._img.paste(region, logo_position)

    def save(self, stream, format=None, **kwargs):
        if format is None:
            format = kwargs.get("kind", self.kind)
        if "kind" in kwargs:
            del kwargs["kind"]
        self._img.save(stream, format=format, **kwargs)

    def __getattr__(self, name):
        return getattr(self._img, name)
