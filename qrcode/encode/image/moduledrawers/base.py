from __future__ import absolute_import

import abc


class QRModuleDrawer(abc.ABC):

    needs_neighbors = False

    def __init__(self, **kwargs):
        pass

    def initialize(self, img: "BaseImage") -> None:
        self.img = img

    @abc.abstractmethod
    def drawrect(self, box, is_active) -> None:
        ...
