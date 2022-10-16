import abc


class QRModuleDrawer(abc.ABC):

    needsNeighbors = False

    def __init__(self, **kwargs):
        pass

    def initialize(self, img: "BaseImage") -> None:
        self.img = img

    @abc.abstractmethod
    def drawrect(self, box, isActive) -> None:
        ...
