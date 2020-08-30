# -*- coding: utf-8 -*-
# =============================================================================
# Created on Sat Aug  1 00:58:23 2020
#
# @author: Brénainn Woodsend
#
# template.py
# What does this file do.
# Copyright (C) 2019-2020  Brénainn Woodsend
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# =============================================================================

"""
"""

import github
import requests
from pathlib import Path

DATA_DIR = Path(__file__).absolute().parents[1] / "data" / "sniffs"

def download(url, dest):
    with open(dest, "wb") as f:
        f.write(requests.get(url).content)
    print(url, "->", "\n  ", dest)

def download_asset(asset, lazy=True):
    dest = DATA_DIR / asset.name
    if lazy and dest.exists():
        return
    download(asset.browser_download_url, dest)


repo = github.Github().get_repo("bwoodsend/pyinstaller-hook-factory")


def download_release(release):
    if not isinstance(release, github.GitRelease.GitRelease):
        release = repo.get_release(str(release))

    for asset in release.get_assets():
        if asset.name.endswith(".json"):
            download_asset(asset)


def main(release=None):
    if release is not None:
        download_release(release)
    else:
        for release in repo.get_releases().reversed:
            download_release(release)


if __name__ == "__main__":
    import fire
    fire.Fire(main)
    
