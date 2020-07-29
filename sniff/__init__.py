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
import psutil, sys, os
from pathlib import Path

class Sniff(object):

    def __init__(self, setup, body, cleanup=None):
        self.process = psutil.Process()

        setup and setup()
        self.base_binaries = self.open_binaries()
        self.base_modules = set(sys.modules.keys())

        body and body()

        new_binaries = set(self.open_binaries()) - set(self.base_binaries)

        self.new_dlls = [i for i in new_binaries if i.suffix != ".pyd"]
        self.new_pyds = [i for i in new_binaries if i.suffix == ".pyd"]
        modules = set(key for (key, val) in sys.modules.items() if val)

        cleanup and cleanup()

        self.new_modules = sorted(modules - self.base_modules)
        self.base_binaries = list(self.base_binaries)
        self.new_dlls.sort()
        self.new_pyds.sort()

    def open_binaries(self):

        if not psutil.OSX:
            out = (i.path for i in self.process.memory_maps())
        else:
            from sniff.lsof import lsof
            out = lsof(self.process.pid)["NAME"]

        # Some names aren't filenames and should be removed. `os.path.exists`
        # catches OSErrors and returns False in these cases.
        return [Path(i) for i in filter(os.path.exists, out)]

    def to_json(self):
        import json
        return json.dumps(
                {i: getattr(self, i) for i in dir(self) if i.startswith("new")},
                indent="  ", default=str)


if __name__ == "__main__":

    def setup():
        pass

    def test():
        import numpy
        numpy.polynomial.test()

    self = Sniff(setup, test)
    print(self.to_json())
