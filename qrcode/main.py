import sys
from typing import Dict, List, Optional, cast
from bisect import bisect_left
import utils

ModulesType = List[List[Optional[bool]]]
precomputed_qr_blanks: Dict[int, ModulesType] = {}


def copy_2d_array(x):
    return [row[:] for row in x]


def make(data=None, **kwargs):
    qr = QRCode(**kwargs)
    qr.addData(data)
    return qr.make_image()


class QRCode():
    modules: ModulesType
    _version: Optional[int] = None

    def __init__(self,
                 version=None,
                 box_size=10,
                 border=4,
                 mask_pattern=None
                 ):

        if int(box_size) <= 0:
            raise ValueError(
                f"Invalid box size (was {box_size}, expected larger than 0)")
        if int(border) < 0:
            raise ValueError(
                "Invalid border value (was %s, expected 0 or larger than that)" % border
            )
        self.version = version
        self.box_size = int(box_size)
        self.border = int(border)
        self.mask_pattern = mask_pattern
        self.clear()

    def clear(self):
        self.modules = [[]]
        self.modules_count = 0
        self.data_cache = None
        self.data_list = []

    def addData(self, data):
        self.data_list.append(utils.QRData(data))
        self.data_cache = None

    def generateData(self):
        self.bestFit()
        self.makeImpl(False, self.best_mask_pattern())

    def bestFit(self, start=1):
        mode_sizes = utils.mode_sizes_for_version(start)
        buffer = utils.BitBuffer()
        for data in self.data_list:
            buffer.put(data.mode, 4)
            buffer.put(len(data), mode_sizes[data.mode])
            data.write(buffer)

        needed_bits = len(buffer)
        print(utils.BIT_LIMIT_TABLE[0])
        self.version = bisect_left(
            utils.BIT_LIMIT_TABLE[0], needed_bits, start
        )
        if self.version == 41:
            print("Data too long")

        if mode_sizes is not utils.mode_sizes_for_version(self.version):
            self.bestFit(start=self.version)
        return self.version

    def setup_position_probe_pattern(self, row, col):
        for r in range(-1, 8):

            if row + r <= -1 or self.modules_count <= row + r:
                continue

            for c in range(-1, 8):

                if col + c <= -1 or self.modules_count <= col + c:
                    continue

                if (
                    (0 <= r <= 6 and c in {0, 6})
                    or (0 <= c <= 6 and r in {0, 6})
                    or (2 <= r <= 4 and 2 <= c <= 4)
                ):
                    self.modules[row + r][col + c] = True
                else:
                    self.modules[row + r][col + c] = False

    def setup_position_adjust_pattern(self):
        pos = utils.pattern_position(self.version)

        for i in range(len(pos)):

            row = pos[i]

            for j in range(len(pos)):

                col = pos[j]

                if self.modules[row][col] is not None:
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
                            self.modules[row + r][col + c] = True
                        else:
                            self.modules[row + r][col + c] = False

    def setup_timing_pattern(self):
        for r in range(8, self.modules_count - 8):
            if self.modules[r][6] is not None:
                continue
            self.modules[r][6] = r % 2 == 0

        for c in range(8, self.modules_count - 8):
            if self.modules[6][c] is not None:
                continue
            self.modules[6][c] = c % 2 == 0

    def setup_type_info(self, test, mask_pattern):
        data = mask_pattern
        bits = utils.BCH_type_info(data)

        # vertical
        for i in range(15):

            mod = not test and ((bits >> i) & 1) == 1

            if i < 6:
                self.modules[i][8] = mod
            elif i < 8:
                self.modules[i + 1][8] = mod
            else:
                self.modules[self.modules_count - 15 + i][8] = mod

        # horizontal
        for i in range(15):

            mod = not test and ((bits >> i) & 1) == 1

            if i < 8:
                self.modules[8][self.modules_count - i - 1] = mod
            elif i < 9:
                self.modules[8][15 - i - 1 + 1] = mod
            else:
                self.modules[8][15 - i - 1] = mod

        # fixed module
        self.modules[self.modules_count - 8][8] = not test

    def setup_type_number(self, test):
        bits = utils.BCH_type_number(self.version)

        for i in range(18):
            mod = not test and ((bits >> i) & 1) == 1
            self.modules[i // 3][i % 3 + self.modules_count - 8 - 3] = mod

        for i in range(18):
            mod = not test and ((bits >> i) & 1) == 1
            self.modules[i % 3 + self.modules_count - 8 - 3][i // 3] = mod

    def map_data(self, data, mask_pattern):
        inc = -1
        row = self.modules_count - 1
        bitIndex = 7
        byteIndex = 0

        mask_func = utils.mask_func(mask_pattern)

        data_len = len(data)

        for col in range(self.modules_count - 1, 0, -2):

            if col <= 6:
                col -= 1

            col_range = (col, col - 1)

            while True:

                for c in col_range:

                    if self.modules[row][c] is None:

                        dark = False

                        if byteIndex < data_len:
                            dark = ((data[byteIndex] >> bitIndex) & 1) == 1

                        if mask_func(row, c):
                            dark = not dark

                        self.modules[row][c] = dark
                        bitIndex -= 1

                        if bitIndex == -1:
                            byteIndex += 1
                            bitIndex = 7

                row += inc

                if row < 0 or self.modules_count <= row:
                    row -= inc
                    inc = -inc
                    break

    def makeImpl(self, test, mask_pattern):
        self.modules_count = self.version * 4 + 17

        if self.version in precomputed_qr_blanks:
            self.modules = copy_2d_array(precomputed_qr_blanks[self.version])
        else:
            self.modules = [
                [None] * self.modules_count for i in range(self.modules_count)
            ]
            self.setup_position_probe_pattern(0, 0)
            self.setup_position_probe_pattern(self.modules_count - 7, 0)
            self.setup_position_probe_pattern(0, self.modules_count - 7)
            self.setup_position_adjust_pattern()
            self.setup_timing_pattern()

            precomputed_qr_blanks[self.version] = copy_2d_array(self.modules)

        self.setup_type_info(test, mask_pattern)

        if self.version >= 7:
            self.setup_type_number(test)

        if self.data_cache is None:
            self.data_cache = utils.create_data(
                self.version, self.data_list
            )
        self.map_data(self.data_cache, mask_pattern)

    def best_mask_pattern(self):
        min_lost_point = 0
        pattern = 0

        for i in range(8):
            self.makeImpl(True, i)

            lost_point = utils.lost_point(self.modules)

            if i == 0 or min_lost_point > lost_point:
                min_lost_point = lost_point
                pattern = i

        return pattern

    def print_ascii(self, out=None, tty=False, invert=False):
        if out is None:
            out = sys.stdout

        if tty and not out.isatty():
            raise OSError("Not a tty")

        if self.data_cache is None:
            self.generateData()

        modcount = self.modules_count
        codes = [bytes((code,)).decode("cp437")
                 for code in (255, 223, 220, 219)]
        if tty:
            invert = True
        if invert:
            codes.reverse()

        def get_module(x, y) -> int:
            if invert and self.border and max(x, y) >= modcount + self.border:
                return 1
            if min(x, y) < 0 or max(x, y) >= modcount:
                return 0
            return cast(int, self.modules[x][y])

        for r in range(-self.border, modcount + self.border, 2):
            if tty:
                if not invert or r < modcount + self.border - 1:
                    out.write("\x1b[48;5;232m")  # Background black
                out.write("\x1b[38;5;255m")  # Foreground white
            for c in range(-self.border, modcount + self.border):
                pos = get_module(r, c) + (get_module(r + 1, c) << 1)
                out.write(codes[pos])
            if tty:
                out.write("\x1b[0m")
            out.write("\n")
        out.flush()
