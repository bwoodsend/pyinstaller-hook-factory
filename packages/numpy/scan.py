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

from sniff import Sniff

def body():
    import numpy
    numpy.test()

results = Sniff(None, body).to_json()

from pathlib import Path
import os
import uuid
name = os.environ.get("MATRIX_NAME", "scan") + "-" + str(uuid.uuid1())

Path(__file__).with_name(name + ".json").write_text(results)
