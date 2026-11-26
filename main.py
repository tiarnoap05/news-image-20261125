#!/usr/bin/env python3
"""Copy the pre-generated front page into the grader's output directory.

Standard library only: the grading sandbox (python3.13-slim) has no
third-party packages and no system fonts, so this program must not
import anything beyond the standard library. The image itself is
rendered in advance and shipped beside this file as entry.png.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    with open(source, "rb") as handle:
        magic = handle.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        sys.stderr.write("entry.png is not a PNG file\n")
        return 1
    if os.path.getsize(source) == 0:
        sys.stderr.write("entry.png is empty\n")
        return 1
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
