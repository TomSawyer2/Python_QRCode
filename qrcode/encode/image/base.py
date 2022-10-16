import abc
from typing import Any, Dict, Optional, Tuple, Type, Union
from qrcode.encode.image.moduledrawers.base import QRModuleDrawer
from qrcode.encode.main import ActiveWithNeighbors, QRCode


DrawerAliases = Dict[str, Tuple[Type[QRModuleDrawer], Dict[str, Any]]]


class BaseImage:
    """
    Base QRCode image output class.
    """

    kind: Optional[str] = None
    allowedKinds: Optional[Tuple[str]] = None
    needsContext = False
    needsProcessing = False
    needsDrawrect = True

    def __init__(self, border, width, boxSize, *args, **kwargs):
        self.border = border
        self.width = width
        self.boxSize = boxSize
        self.pixelSize = (self.width + self.border * 2) * self.boxSize
        self._img = self.newImage(**kwargs)
        self.initNewImage()

    @abc.abstractmethod
    def drawrect(self, row, col):
        """
        Draw a single rectangle of the QR code.
        """

    @abc.abstractmethod
    def save(self, stream, kind=None):
        """
        Save the image file.
        """

    def pixelBox(self, row, col):
        """
        A helper method for pixel-based image generators that specifies the
        four pixel coordinates for a single rect.
        """
        x = (col + self.border) * self.boxSize
        y = (row + self.border) * self.boxSize
        return (
            (x, y),
            (x + self.boxSize - 1, y + self.boxSize - 1),
        )

    @abc.abstractmethod
    def newImage(self, **kwargs) -> Any:
        """
        Build the image class. Subclasses should return the class created.
        """

    def initNewImage(self):
        pass

    def get_image(self, **kwargs):
        """
        Return the image class for further processing.
        """
        return self._img

    def checkKind(self, kind, transform=None):
        """
        Get the image type.
        """
        if kind is None:
            kind = self.kind
        allowed = not self.allowedKinds or kind in self.allowedKinds
        if transform:
            kind = transform(kind)
            if not allowed:
                allowed = kind in self.allowedKinds
        if not allowed:
            raise ValueError(
                f"Cannot set {type(self).__name__} type to {kind}")
        return kind

    def isEye(self, row: int, col: int):
        """
        Find whether the referenced module is in an eye.
        """
        return (
            (row < 7 and col < 7)
            or (row < 7 and self.width - col < 8)
            or (self.width - row < 8 and col < 7)
        )


class BaseImageWithDrawer(BaseImage):
    defaultDrawerClass: Type[QRModuleDrawer]
    drawerAliases: DrawerAliases = {}

    def getDefaultModuleDrawer(self) -> QRModuleDrawer:
        return self.defaultDrawerClass()

    def getDefaultEyeDrawer(self) -> QRModuleDrawer:
        return self.defaultDrawerClass()

    needsContext = True

    moduleDrawer: "QRModuleDrawer"
    eyeDrawer: "QRModuleDrawer"

    def __init__(
        self,
        *args,
        moduleDrawer: Union[QRModuleDrawer, str, None] = None,
        eyeDrawer: Union[QRModuleDrawer, str, None] = None,
        **kwargs,
    ):
        self.moduleDrawer = (
            self.getDrawer(moduleDrawer) or self.getDefaultModuleDrawer()
        )
        self.eyeDrawer = self.getDrawer(
            eyeDrawer) or self.getDefaultEyeDrawer()
        super().__init__(*args, **kwargs)

    def getDrawer(
        self, drawer: Union[QRModuleDrawer, str, None]
    ) -> Optional[QRModuleDrawer]:
        if not isinstance(drawer, str):
            return drawer
        drawerCls, kwargs = self.drawerAliases[drawer]
        return drawerCls(**kwargs)

    def initNewImage(self):
        self.moduleDrawer.initialize(img=self)
        self.eyeDrawer.initialize(img=self)

        return super().initNewImage()

    def drawrectContext(self, row: int, col: int, qr: "QRCode"):
        box = self.pixelBox(row, col)
        drawer = self.eyeDrawer if self.isEye(
            row, col) else self.moduleDrawer
        isActive: Union[bool, ActiveWithNeighbors] = (
            qr.activeWithNeighbors(row, col)
            if drawer.needsNeighbors
            else False
        )

        drawer.drawrect(box, isActive)
