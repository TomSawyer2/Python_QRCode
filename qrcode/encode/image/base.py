import abc
from typing import Any, Dict, Optional, Tuple, Type, Union
from qrcode.encode.image.moduledrawers.base import QRModuleDrawer
from qrcode.encode.main import ActiveWithNeighbors, QRCode


DrawerAliases = Dict[str, Tuple[Type[QRModuleDrawer], Dict[str, Any]]]


class BaseImage:
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
        二维码绘制矩形
        """

    @abc.abstractmethod
    def save(self, stream, kind=None):
        """
        保存图片
        """

    def pixelBox(self, row, col):
        x = (col + self.border) * self.boxSize
        y = (row + self.border) * self.boxSize
        return [
            (x, y),
            (x + self.boxSize - 1, y + self.boxSize - 1),
        ]

    @abc.abstractmethod
    def newImage(self, **kwargs) -> Any:
        """
        新建Image类
        """

    def initNewImage(self):
        pass

    def get_image(self, **kwargs):
        """
        返回类内的图片
        """
        return self._img

    def checkKind(self, kind, transform=None):
        """
        检查图片类型
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
