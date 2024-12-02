#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import zip_longest

# adaptive tables
# TODO
# 1. allow length reset after one screen has passed (24/25 rows)
# 2. allow ignoring outliers


class ATable:

    def __init__(self, max_row_lenght=88, delimiter=" "):
        self.col_lens = []
        self.delimiter = delimiter

    def update_lens(self, *cols):
        new_lens = [len(col) for col in cols]
        zips = zip_longest(self.col_lens, new_lens, fillvalue=0)
        self.col_lens = [max(zp) for zp in zips]

    def only_print(self, *cols):
        parts = []
        for col, length in zip(cols, self.col_lens):
            parts.append(col.ljust(length))
        print(self.delimiter.join(parts))

    def print(self, *cols):
        cols = [str(col) for col in cols]
        self.update_lens(*cols)
        self.only_print(*cols)

    def reset(self):
        self.col_lens = []
