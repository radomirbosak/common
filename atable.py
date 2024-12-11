#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import astuple, fields, is_dataclass
from itertools import zip_longest
import unicodedata

# adaptive tables
# TODO
# 1. allow length reset after one screen has passed (24/25 rows)
# 2. allow ignoring outliers
# 3. delayed printing using flush/second thread
# 4. liquid columned priting of narrow lists/tables
# 5. allow searching through log history
# 6. automatically print small info where waiting occurs
# 7. right/center alignment
# 8. handle colors/ANSI codes
# 9. consider switching to tabulate


def update_lens(old_lens, *cols, len_fn=len):
    new_lens = [len_fn(col) for col in cols]
    zips = zip_longest(old_lens, new_lens, fillvalue=0)
    return [max(zp) for zp in zips]


class ATable:

    def __init__(self, max_row_lenght=88, delimiter="  ", asian_chars=True):
        self.col_lens = []
        self.delimiter = delimiter

        # asian chars adjustment
        self.asian_chars = asian_chars
        self.len = visual_len if self.asian_chars else len
        self.ljust = (
            fw_ljust if self.asian_chars else lambda text, length: text.ljust(length)
        )

    def update_lens(self, *cols):
        self.col_lens = update_lens(self.col_lens, *cols, len_fn=self.len)

    def only_print(self, *cols):
        parts = []
        for col, length in zip(cols, self.col_lens):
            parts.append(self.ljust(col, length))
        print(self.delimiter.join(parts))

    def print(self, *cols):
        if len(cols) == 1 and is_dataclass(cols[0]):
            cols = astuple(cols[0])
        cols = [str(col) for col in cols]
        self.update_lens(*cols)
        self.only_print(*cols)

    def print_header(self, *cols, header_separator="="):
        if len(cols) == 1 and is_dataclass(cols[0]):
            cols = [field.name for field in fields(cols[0])]
        sep_row = [header_separator * len(col) for col in cols]
        self.print(*cols)
        self.print(*sep_row)

    def reset(self):
        self.col_lens = []


class SlidingResetATable(ATable):
    def __init__(self, *args, reset_window=100, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.reset_window = reset_window
        self.print_counter = 0
        self.sliding_lens = []

    def print(self, *cols):
        super().print(*cols)
        self.print_counter += 1

        if self.print_counter % self.reset_window == 0:
            self.col_lens = self.sliding_lens
            self.sliding_lens = []

    def update_lens(self, *cols):
        super().update_lens(*cols)
        self.sliding_lens = update_lens(self.sliding_lens, *cols, len_fn=self.len)



def visual_len(text):
    WIDTH_MAP = {"W": 2, "Na": 1, "N": 1, "F": 2, "A": 1}
    return sum(WIDTH_MAP[unicodedata.east_asian_width(char)] for char in text)


def fw_ljust(text, width):
    vlen = visual_len(text)
    if vlen >= width:
        return text
    return text + " " * (width - vlen)
