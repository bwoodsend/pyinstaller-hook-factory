# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2005-2020, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License (version 2
# or later) with exception for distributing the bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#
# SPDX-License-Identifier: (GPL-2.0-or-later WITH Bootloader-exception)
#-----------------------------------------------------------------------------

"""

"""

from pathlib import Path
import subprocess


def lsof(pid):
    """Run ``lsof -p $pid``, parse the output and return a :class:`LsofParse`
    object.
    """
    status, output = subprocess.getstatusoutput("lsof -p %i" % pid)
    if status:
        raise OSError(output)
    return LsofParse(output)


class LsofParse(object):
    """Parse the output of a ``lsof $pid`` command on a OSX machine.
    """
    def __init__(self, raw):
        self.raw = raw
        self._lines = self.raw.split("\n")
        self._parse()

    def _parse(self):
        self._strip()
        self._find_seperator_indices()
        self._parse_tabular()

    def _strip(self):
        "Remove irrelavent lines before and empty lines after the main body."
        for (i, head) in enumerate(self._lines):
            if head.startswith("COMMAND "):
                break
        else:
            raise ValueError("Failed to find header.")

        self._lines = self._lines[i:]
        while not self._lines[-1]:
            self._lines.pop(-1)

    def _find_seperator_indices(self):
        """Cells in each row are seperated by spaces but may also contain
        spaces. Find str indices that are spaces in every row. i.e. satisfy
        ``all(line[idx] == " " for line in self._lines)``. Except this should be
        generalised to accomodate line length mismatch:
        ``all(len(line) >= idx or line[idx] == " " for line in self._lines)``.
        """
        self._always_space = [True] * max(len(i.rstrip()) for i in self._lines)
        # Using rstrip() above ensures that the `self._always_space[i + 1]`
        # will never raise an IndexError.

        for line in self._lines:
            for (i, char) in enumerate(line):
                if char != " ":
                    self._always_space[i] = False

        # Enumerate, removing consecutive all-space columns.
        self._seperators = [i for (i, x) in enumerate(self._always_space)
                            if x and not (self._always_space[i + 1])]


    def _parse_tabular(self):
        "Finally read the table into a list of lists."
        self.table = []
        for line in self._lines:
            row = []
            start = 0
            for end in self._seperators:
                row.append(line[start:end].strip())
                start = end
            row.append(line[start:].strip())
            self.table.append(row)
        self.head, *self.table = self.table
        self.column_numbers = {j: i for (i, j) in enumerate(self.head)}

    def __getitem__(self, x):
        if isinstance(x, str):
            index = self.column_numbers[x]
            return [row[index] for row in self.table]
        return self.table[x]


if __name__ == "__main__":
    raw = (Path(__file__).absolute().parent.parent
           / "data" / "lsof-output" / "a.log").read_text()

    self = LsofParse(raw)

