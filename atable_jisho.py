#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import astuple, fields, is_dataclass
from itertools import zip_longest

from jstring import fw_ljust, visual_len

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


class ATable:

    def __init__(self, max_row_lenght=88, delimiter=" ", asian_chars=True):
        self.col_lens = []
        self.delimiter = delimiter
        self.asian_chars = asian_chars

    def update_lens(self, *cols):
        used_len = visual_len if self.asian_chars else len
        new_lens = [used_len(col) for col in cols]
        zips = zip_longest(self.col_lens, new_lens, fillvalue=0)
        self.col_lens = [max(zp) for zp in zips]

    def only_print(self, *cols):
        parts = []
        for col, length in zip(cols, self.col_lens):
            adjusted = fw_ljust(col, length) if self.asian_chars else col.ljust(length)
            parts.append(adjusted)
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
