# pyinstaller-hook-factory

A dumping ground for CI tests for [PyInstaller](https://www.pyinstaller.org/) hooks for some of the less PyInstaller friendly packages.

CI tests aim to cover as many cases as possible:
- Installation method:
  - Plain Python with package installed by pip.
  - Anaconda Python with package installed by Conda.
  - Anaconda Python with package installed by pip.
- OS:
  - Windows
  - macOS
  - Linux
- Package version
- Python version (rarely an issue)

The end goal is to be able to test new versions of packages as they come out and fix any issues ASAP.
