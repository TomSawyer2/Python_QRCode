from typing import NamedTuple
import LUT

EXP_TABLE = list(range(256))

LOG_TABLE = list(range(256))

for i in range(8):
    EXP_TABLE[i] = 1 << i

for i in range(8, 256):
    EXP_TABLE[i] = (
        EXP_TABLE[i - 4] ^ EXP_TABLE[i - 5] ^ EXP_TABLE[i - 6] ^ EXP_TABLE[i - 8]
    )

for i in range(255):
    LOG_TABLE[EXP_TABLE[i]] = i


def glog(n):
    if n < 1:  # pragma: no cover
        raise ValueError(f"glog({n})")
    return LOG_TABLE[n]


def gexp(n):
    return EXP_TABLE[n % 255]


class Polynomial:
    def __init__(self, num, shift):
        if not num:
            raise ValueError(f"Polynomial({num}, {shift})")

        offset = 0
        for offset in range(len(num)):
            if num[offset] != 0:
                break

        self.num = num[offset:] + [0] * shift

    def __getitem__(self, index):
        return self.num[index]

    def __iter__(self):
        return iter(self.num)

    def __len__(self):
        return len(self.num)

    def __mul__(self, other):
        num = [0] * (len(self) + len(other) - 1)

        for i, item in enumerate(self):
            for j, other_item in enumerate(other):
                num[i + j] ^= gexp(glog(item) + glog(other_item))

        return Polynomial(num, 0)

    def __mod__(self, other):
        difference = len(self) - len(other)
        if difference < 0:
            return self

        ratio = glog(self[0]) - glog(other[0])

        num = [
            item ^ gexp(glog(other_item) + ratio)
            for item, other_item in zip(self, other)
        ]
        if difference:
            num.extend(self[-difference:])

        # recursive call
        return Polynomial(num, 0) % other


class RSBlock(NamedTuple):
    totalCount: int
    dataCount: int


def rsBlocks(version):
    offset = 1
    rsBlock = LUT.RS_BLOCK_TABLE[(version - 1) * 4 + offset]

    blocks = []

    for i in range(0, len(rsBlock), 3):
        count, totalCount, dataCount = rsBlock[i : i + 3]
        for _ in range(count):
            blocks.append(RSBlock(totalCount, dataCount))

    return blocks
