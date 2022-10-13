import sys
from typing import Dict, List, Optional, cast
from bisect import bisect_left
import utils

PixelsType = List[List[Optional[bool]]]
preComputedQrBlanks: Dict[int, PixelsType] = {}


def copy2dArray(x):
    return [row[:] for row in x]


class QRCode():
    pixels: PixelsType

    def __init__(self,
                 version=None,
                 border=4,
                 maskPattern=None
                 ):

        if int(border) < 0:
            print("Border must be non-negative")
            sys.exit(1)
        self.version = version
        self.border = int(border)
        self.maskPattern = maskPattern
        self.clear()

    def clear(self):
        self.pixels = [[]]
        self.pixelsCount = 0
        self.dataCache = None
        self.dataList = []

    def addData(self, data):
        self.dataList.append(utils.QRData(data))
        self.dataCache = None

    def generateData(self):
        self.bestFit()
        self.makeImpl(False, self.bestMaskPattern())

    def bestFit(self, start=1):
        mode_sizes = utils.getModeSizesForVersion(start)
        buffer = utils.BitBuffer()
        for data in self.dataList:
            buffer.put(data.mode, 4)
            buffer.put(len(data), mode_sizes[data.mode])
            data.write(buffer)

        needed_bits = len(buffer)
        self.version = bisect_left(
            utils.BIT_LIMIT_TABLE[0], needed_bits, start
        )
        if self.version == 41:
            print("Data too long for a QR code")
            sys.exit(1)

        if mode_sizes is not utils.getModeSizesForVersion(self.version):
            self.bestFit(start=self.version)
        return self.version

    def setupPositionProbePattern(self, row, col):
        for r in range(-1, 8):

            if row + r <= -1 or self.pixelsCount <= row + r:
                continue

            for c in range(-1, 8):

                if col + c <= -1 or self.pixelsCount <= col + c:
                    continue

                if (
                    (0 <= r <= 6 and c in {0, 6})
                    or (0 <= c <= 6 and r in {0, 6})
                    or (2 <= r <= 4 and 2 <= c <= 4)
                ):
                    self.pixels[row + r][col + c] = True
                else:
                    self.pixels[row + r][col + c] = False

    def setupPositionAdjustPattern(self):
        pos = utils.patternPosition(self.version)

        for i in range(len(pos)):

            row = pos[i]

            for j in range(len(pos)):

                col = pos[j]

                if self.pixels[row][col] is not None:
                    continue

                for r in range(-2, 3):

                    for c in range(-2, 3):

                        if (
                            r == -2
                            or r == 2
                            or c == -2
                            or c == 2
                            or (r == 0 and c == 0)
                        ):
                            self.pixels[row + r][col + c] = True
                        else:
                            self.pixels[row + r][col + c] = False

    def setupTimingPattern(self):
        for r in range(8, self.pixelsCount - 8):
            if self.pixels[r][6] is not None:
                continue
            self.pixels[r][6] = r % 2 == 0

        for c in range(8, self.pixelsCount - 8):
            if self.pixels[6][c] is not None:
                continue
            self.pixels[6][c] = c % 2 == 0

    def setupTypeInfo(self, test, maskPattern):
        data = maskPattern
        bits = utils.BCHTypeInfo(data)

        # in vertical
        for i in range(15):

            mod = not test and ((bits >> i) & 1) == 1

            if i < 6:
                self.pixels[i][8] = mod
            elif i < 8:
                self.pixels[i + 1][8] = mod
            else:
                self.pixels[self.pixelsCount - 15 + i][8] = mod

        # in horizontal
        for i in range(15):

            mod = not test and ((bits >> i) & 1) == 1

            if i < 8:
                self.pixels[8][self.pixelsCount - i - 1] = mod
            elif i < 9:
                self.pixels[8][15 - i - 1 + 1] = mod
            else:
                self.pixels[8][15 - i - 1] = mod

        # fixed module
        self.pixels[self.pixelsCount - 8][8] = not test

    def setupTypeNumber(self, test):
        bits = utils.BCH_type_number(self.version)

        for i in range(18):
            mod = not test and ((bits >> i) & 1) == 1
            self.pixels[i // 3][i % 3 + self.pixelsCount - 8 - 3] = mod

        for i in range(18):
            mod = not test and ((bits >> i) & 1) == 1
            self.pixels[i % 3 + self.pixelsCount - 8 - 3][i // 3] = mod

    def mapData(self, data, maskPattern):
        inc = -1
        row = self.pixelsCount - 1
        bitIndex = 7
        byteIndex = 0

        getMaskFunc = utils.getMaskFunc(maskPattern)

        for col in range(self.pixelsCount - 1, 0, -2):

            if col <= 6:
                col -= 1

            col_range = (col, col - 1)

            while True:

                for c in col_range:

                    if self.pixels[row][c] is None:

                        dark = False

                        if byteIndex < len(data):
                            dark = ((data[byteIndex] >> bitIndex) & 1) == 1

                        if getMaskFunc(row, c):
                            dark = not dark

                        self.pixels[row][c] = dark
                        bitIndex -= 1

                        if bitIndex == -1:
                            byteIndex += 1
                            bitIndex = 7

                row += inc

                if row < 0 or self.pixelsCount <= row:
                    row -= inc
                    inc = -inc
                    break

    def makeImpl(self, test, maskPattern):
        self.pixelsCount = self.version * 4 + 17

        if self.version in preComputedQrBlanks:
            self.pixels = copy2dArray(preComputedQrBlanks[self.version])
        else:
            self.pixels = [
                [None] * self.pixelsCount for i in range(self.pixelsCount)
            ]
            self.setupPositionProbePattern(0, 0)
            self.setupPositionProbePattern(self.pixelsCount - 7, 0)
            self.setupPositionProbePattern(0, self.pixelsCount - 7)
            self.setupPositionAdjustPattern()
            self.setupTimingPattern()

            preComputedQrBlanks[self.version] = copy2dArray(self.pixels)

        self.setupTypeInfo(test, maskPattern)

        if self.version >= 7:
            self.setupTypeNumber(test)

        if self.dataCache is None:
            self.dataCache = utils.create_data(
                self.version, self.dataList
            )
        self.mapData(self.dataCache, maskPattern)

    def bestMaskPattern(self):
        min_lostPoint = 0
        pattern = 0

        for i in range(8):
            self.makeImpl(True, i)

            lostPoint = utils.lostPoint(self.pixels)

            if i == 0 or min_lostPoint > lostPoint:
                min_lostPoint = lostPoint
                pattern = i

        return pattern

    def printAscii(self, out=None, tty=False, invert=False):
        if out is None:
            out = sys.stdout

        if tty and not out.isatty():
            raise OSError("Not a tty")

        if self.dataCache is None:
            self.generateData()

        modcount = self.pixelsCount
        codes = [bytes((code,)).decode("cp437")
                 for code in (255, 223, 220, 219)]
        if tty:
            invert = True
        if invert:
            codes.reverse()

        def getModule(x, y) -> int:
            if invert and self.border and max(x, y) >= modcount + self.border:
                return 1
            if min(x, y) < 0 or max(x, y) >= modcount:
                return 0
            return cast(int, self.pixels[x][y])

        for r in range(-self.border, modcount + self.border, 2):
            if tty:
                if not invert or r < modcount + self.border - 1:
                    out.write("\x1b[48;5;232m")  # Background black
                out.write("\x1b[38;5;255m")  # Foreground white
            for c in range(-self.border, modcount + self.border):
                pos = getModule(r, c) + (getModule(r + 1, c) << 1)
                out.write(codes[pos])
            if tty:
                out.write("\x1b[0m")
            out.write("\n")
        out.flush()
