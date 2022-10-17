import math
import re
from typing import List
import qrcode.encode.LUT as LUT
import qrcode.encode.polynomial as polynomial
from qrcode.encode.polynomial import Polynomial, gexp

# 二维码编码模式
MODE_NUMBER = 1 << 0
MODE_ALPHA_NUM = 1 << 1
MODE_8BIT_BYTE = 1 << 2
MODE_KANJI = 1 << 3

# 编码模式对应的大小
MODE_SIZE_SMALL = {
    MODE_NUMBER: 10,
    MODE_ALPHA_NUM: 9,
    MODE_8BIT_BYTE: 8,
    MODE_KANJI: 8,
}
MODE_SIZE_MEDIUM = {
    MODE_NUMBER: 12,
    MODE_ALPHA_NUM: 11,
    MODE_8BIT_BYTE: 16,
    MODE_KANJI: 10,
}
MODE_SIZE_LARGE = {
    MODE_NUMBER: 14,
    MODE_ALPHA_NUM: 13,
    MODE_8BIT_BYTE: 16,
    MODE_KANJI: 12,
}

ALPHA_NUM = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
RE_ALPHA_NUM = re.compile(b"^[" + re.escape(ALPHA_NUM) + rb"]*\Z")

NUMBER_LENGTH = {3: 10, 2: 7, 1: 4}

PATTERN_POSITION_TABLE = [
    [],
    [6, 18],
    [6, 22],
    [6, 26],
    [6, 30],
    [6, 34],
    [6, 22, 38],
    [6, 24, 42],
    [6, 26, 46],
    [6, 28, 50],
    [6, 30, 54],
    [6, 32, 58],
    [6, 34, 62],
    [6, 26, 46, 66],
    [6, 26, 48, 70],
    [6, 26, 50, 74],
    [6, 30, 54, 78],
    [6, 30, 56, 82],
    [6, 30, 58, 86],
    [6, 34, 62, 90],
    [6, 28, 50, 72, 94],
    [6, 26, 50, 74, 98],
    [6, 30, 54, 78, 102],
    [6, 28, 54, 80, 106],
    [6, 32, 58, 84, 110],
    [6, 30, 58, 86, 114],
    [6, 34, 62, 90, 118],
    [6, 26, 50, 74, 98, 122],
    [6, 30, 54, 78, 102, 126],
    [6, 26, 52, 78, 104, 130],
    [6, 30, 56, 82, 108, 134],
    [6, 34, 60, 86, 112, 138],
    [6, 30, 58, 86, 114, 142],
    [6, 34, 62, 90, 118, 146],
    [6, 30, 54, 78, 102, 126, 150],
    [6, 24, 50, 76, 102, 128, 154],
    [6, 28, 54, 80, 106, 132, 158],
    [6, 32, 58, 84, 110, 136, 162],
    [6, 26, 54, 82, 110, 138, 166],
    [6, 30, 58, 86, 114, 142, 170],
]

G15 = (1 << 10) | (1 << 8) | (1 << 5) | (
    1 << 4) | (1 << 2) | (1 << 1) | (1 << 0)
G18 = (
    (1 << 12)
    | (1 << 11)
    | (1 << 10)
    | (1 << 9)
    | (1 << 8)
    | (1 << 5)
    | (1 << 2)
    | (1 << 0)
)
G15_MASK = (1 << 14) | (1 << 12) | (1 << 10) | (1 << 4) | (1 << 1)

PAD0 = 0xEC
PAD1 = 0x11


def dataCount(block):
    return block.dataCount


BIT_LIMIT_TABLE = [
    [0]
    + [
        8 * sum(map(dataCount, polynomial.rsBlocks(version)))
        for version in range(1, 41)
    ]
]
def _data_count(block): return block.dataCount


BIT_LIMIT_TABLE = [
    [0] + [8*sum(map(_data_count, polynomial.rsBlocks(version)))
           for version in range(1, 41)]
]


def BCHTypeInfo(data):
    d = data << 10
    while BCHDigit(d) - BCHDigit(G15) >= 0:
        d ^= G15 << (BCHDigit(d) - BCHDigit(G15))

    return ((data << 10) | d) ^ G15_MASK


def BCH_type_number(data):
    d = data << 12
    while BCHDigit(d) - BCHDigit(G18) >= 0:
        d ^= G18 << (BCHDigit(d) - BCHDigit(G18))
    return (data << 12) | d


def BCHDigit(data):
    digit = 0
    while data != 0:
        digit += 1
        data >>= 1
    return digit


def patternPosition(version):
    return PATTERN_POSITION_TABLE[version - 1]


def getMaskFunc(pattern):
    """
    返回maskPattern对应的函数
    :param pattern: Mask pattern (0-7)
    :return: Mask function
    """
    if pattern == 0:  # 000
        return lambda i, j: (i + j) % 2 == 0
    if pattern == 1:  # 001
        return lambda i, j: i % 2 == 0
    if pattern == 2:  # 010
        return lambda i, j: j % 3 == 0
    if pattern == 3:  # 011
        return lambda i, j: (i + j) % 3 == 0
    if pattern == 4:  # 100
        return lambda i, j: (math.floor(i / 2) + math.floor(j / 3)) % 2 == 0
    if pattern == 5:  # 101
        return lambda i, j: (i * j) % 2 + (i * j) % 3 == 0
    if pattern == 6:  # 110
        return lambda i, j: ((i * j) % 2 + (i * j) % 3) % 2 == 0
    if pattern == 7:  # 111
        return lambda i, j: ((i * j) % 3 + (i + j) % 2) % 2 == 0
    print("bad mask pattern: %s" % pattern)
    return None


def getModeSizesForVersion(version):
    if version < 10:
        return MODE_SIZE_SMALL
    elif version < 27:
        return MODE_SIZE_MEDIUM
    else:
        return MODE_SIZE_LARGE


def getLengthInBits(mode, version):
    if mode not in (MODE_NUMBER, MODE_ALPHA_NUM, MODE_8BIT_BYTE):
        print("Invalid mode: %s" % mode)
        return 0

    checkVersion(version)

    return getModeSizesForVersion(version)[mode]


def checkVersion(version):
    if version < 1 or version > 40:
        print("Invalid version: %s" % version)
        return False


def lostPoint(modules):

    modulesCount = len(modules)

    lostPoint = 0

    lostPoint = lostPointLevelA(modules, modulesCount)
    lostPoint += lostPointLevelB(modules, modulesCount)
    lostPoint += lostPointLevelC(modules, modulesCount)
    lostPoint += lostPointLevelD(modules, modulesCount)

    return lostPoint


def lostPointLevelA(modules, modulesCount):
    lostPoint = 0

    modulesRange = range(modulesCount)
    container = [0] * (modulesCount + 1)

    for row in modulesRange:
        currentRow = modules[row]
        previousColor = currentRow[0]
        length = 0
        for col in modulesRange:
            if currentRow[col] == previousColor:
                length += 1
            else:
                if length >= 5:
                    container[length] += 1
                length = 1
                previousColor = currentRow[col]
        if length >= 5:
            container[length] += 1

    for col in modulesRange:
        previousColor = modules[0][col]
        length = 0
        for row in modulesRange:
            if modules[row][col] == previousColor:
                length += 1
            else:
                if length >= 5:
                    container[length] += 1
                length = 1
                previousColor = modules[row][col]
        if length >= 5:
            container[length] += 1

    lostPoint += sum(
        container[eachLength] * (eachLength - 2)
        for eachLength in range(5, modulesCount + 1)
    )

    return lostPoint


def lostPointLevelB(modules, modulesCount):
    lostPoint = 0

    modulesRange = range(modulesCount - 1)
    for row in modulesRange:
        currentRow = modules[row]
        nextRow = modules[row + 1]
        modulesRange_iter = iter(modulesRange)
        for col in modulesRange_iter:
            topRight = currentRow[col + 1]
            if topRight != nextRow[col + 1]:
                next(modulesRange_iter, None)
            elif topRight != currentRow[col]:
                continue
            elif topRight != nextRow[col]:
                continue
            else:
                lostPoint += 3

    return lostPoint


def lostPointLevelC(modules, modulesCount):
    modulesRange = range(modulesCount)
    modulesRange_short = range(modulesCount - 10)
    lostPoint = 0

    for row in modulesRange:
        currentRow = modules[row]
        modulesRangeShortIter = iter(modulesRange_short)
        col = 0
        for col in modulesRangeShortIter:
            if (
                not currentRow[col + 1]
                and currentRow[col + 4]
                and not currentRow[col + 5]
                and currentRow[col + 6]
                and not currentRow[col + 9]
                and (
                    currentRow[col + 0]
                    and currentRow[col + 2]
                    and currentRow[col + 3]
                    and not currentRow[col + 7]
                    and not currentRow[col + 8]
                    and not currentRow[col + 10]
                    or not currentRow[col + 0]
                    and not currentRow[col + 2]
                    and not currentRow[col + 3]
                    and currentRow[col + 7]
                    and currentRow[col + 8]
                    and currentRow[col + 10]
                )
            ):
                lostPoint += 40
            if currentRow[col + 10]:
                next(modulesRangeShortIter, None)

    for col in modulesRange:
        modulesRangeShortIter = iter(modulesRange_short)
        row = 0
        for row in modulesRangeShortIter:
            if (
                not modules[row + 1][col]
                and modules[row + 4][col]
                and not modules[row + 5][col]
                and modules[row + 6][col]
                and not modules[row + 9][col]
                and (
                    modules[row + 0][col]
                    and modules[row + 2][col]
                    and modules[row + 3][col]
                    and not modules[row + 7][col]
                    and not modules[row + 8][col]
                    and not modules[row + 10][col]
                    or not modules[row + 0][col]
                    and not modules[row + 2][col]
                    and not modules[row + 3][col]
                    and modules[row + 7][col]
                    and modules[row + 8][col]
                    and modules[row + 10][col]
                )
            ):
                lostPoint += 40
            if modules[row + 10][col]:
                next(modulesRangeShortIter, None)

    return lostPoint


def lostPointLevelD(modules, modulesCount):
    darkCount = sum(map(sum, modules))
    percent = float(darkCount) / (modulesCount ** 2)
    rating = int(abs(percent * 100 - 50) / 5)
    return rating * 10


def toBytestring(data):
    if not isinstance(data, bytes):
        data = str(data).encode("utf-8")
    return data


def optimalMode(data):
    if data.isdigit():
        return MODE_NUMBER
    if RE_ALPHA_NUM.match(data):
        return MODE_ALPHA_NUM
    return MODE_8BIT_BYTE


class QRData:

    def __init__(self, data, mode=None, check_data=True):
        if check_data:
            data = toBytestring(data)

        if mode is None:
            self.mode = optimalMode(data)
        else:
            self.mode = mode
            if mode not in (MODE_NUMBER, MODE_ALPHA_NUM, MODE_8BIT_BYTE):
                print("Invalid mode: %s" % mode)
                return False
            if check_data and mode < optimalMode(data):  # pragma: no cover
                print("Data is not compatible with mode")
                return False

        self.data = data

    def __len__(self):
        return len(self.data)

    def write(self, buffer):
        if self.mode == MODE_NUMBER:
            for i in range(0, len(self.data), 3):
                chars = self.data[i: i + 3]
                bit_length = NUMBER_LENGTH[len(chars)]
                buffer.put(int(chars), bit_length)
        elif self.mode == MODE_ALPHA_NUM:
            for i in range(0, len(self.data), 2):
                chars = self.data[i: i + 2]
                if len(chars) > 1:
                    buffer.put(
                        ALPHA_NUM.find(chars[0]) * 45 +
                        ALPHA_NUM.find(chars[1]), 11
                    )
                else:
                    buffer.put(ALPHA_NUM.find(chars), 6)
        else:
            data = self.data
            for c in data:
                buffer.put(c, 8)

    def __repr__(self):
        return repr(self.data)


class BitBuffer:
    def __init__(self):
        self.buffer: List[int] = []
        self.length = 0

    def __repr__(self):
        return ".".join([str(n) for n in self.buffer])

    def get(self, index):
        bufIdx = math.floor(index / 8)
        return ((self.buffer[bufIdx] >> (7 - index % 8)) & 1) == 1

    def put(self, num, length):
        for i in range(length):
            self.put_bit(((num >> (length - i - 1)) & 1) == 1)

    def __len__(self):
        return self.length

    def put_bit(self, bit):
        bufIdx = self.length // 8
        if len(self.buffer) <= bufIdx:
            self.buffer.append(0)
        if bit:
            self.buffer[bufIdx] |= 0x80 >> (self.length % 8)
        self.length += 1


def createBytes(buffer: BitBuffer, rsBlocks: List[polynomial.RSBlock]):
    offset = 0

    maxDcCount = 0
    maxEcCount = 0

    dcdata = [0] * len(rsBlocks)
    ecdata = [0] * len(rsBlocks)

    for r in range(len(rsBlocks)):

        dcCount = rsBlocks[r].dataCount
        ecCount = rsBlocks[r].totalCount - dcCount

        maxDcCount = max(maxDcCount, dcCount)
        maxEcCount = max(maxEcCount, ecCount)

        dcdata[r] = [0] * dcCount

        for i in range(len(dcdata[r])):
            dcdata[r][i] = 0xff & buffer.buffer[i + offset]
        offset += dcCount

        if ecCount in LUT.RSPOLY_LUT:
            rsPoly = Polynomial(LUT.RSPOLY_LUT[ecCount], 0)
        else:
            rsPoly = Polynomial([1], 0)
            for i in range(ecCount):
                rsPoly = rsPoly * Polynomial([1, gexp(i)], 0)

        rawPoly = Polynomial(dcdata[r], len(rsPoly) - 1)

        modPoly = rawPoly % rsPoly
        ecdata[r] = [0] * (len(rsPoly) - 1)
        for i in range(len(ecdata[r])):
            modIndex = i + len(modPoly) - len(ecdata[r])
            ecdata[r][i] = modPoly[modIndex] if (modIndex >= 0) else 0
    totalCodeCount = sum(rs_block.totalCount for rs_block in rsBlocks)
    data = [None] * totalCodeCount
    index = 0

    for i in range(maxDcCount):
        for r in range(len(rsBlocks)):
            if i < len(dcdata[r]):
                data[index] = dcdata[r][i]
                index += 1

    for i in range(maxEcCount):
        for r in range(len(rsBlocks)):
            if i < len(ecdata[r]):
                data[index] = ecdata[r][i]
                index += 1

    return data


def create_data(version, dataList):

    buffer = BitBuffer()
    for data in dataList:
        buffer.put(data.mode, 4)
        buffer.put(len(data), getLengthInBits(data.mode, version))
        data.write(buffer)

    # 计算版本对应的最大容量
    rsBlocks = polynomial.rsBlocks(version)
    bitLimit = sum(block.dataCount * 8 for block in rsBlocks)
    if len(buffer) > bitLimit:
        print("长度溢出")
        return None

    for _ in range(min(bitLimit - len(buffer), 4)):
        buffer.put_bit(False)

    delimit = len(buffer) % 8
    if delimit:
        for _ in range(8 - delimit):
            buffer.put_bit(False)

    bytes2Fill = (bitLimit - len(buffer)) // 8
    for i in range(bytes2Fill):
        if i % 2 == 0:
            buffer.put(PAD0, 8)
        else:
            buffer.put(PAD1, 8)

    return createBytes(buffer, rsBlocks)
