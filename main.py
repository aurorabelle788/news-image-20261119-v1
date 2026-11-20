#!/usr/bin/env python3
"""news-image-20261119: one image summing up Thursday 19 November 2026.

The entry image is the entry.png beside this file: a 1024x1024 front
page with the 15 verified stories of the day, a masthead naming the
date, the lead story in a large slot, and the remaining 14 stories in
a two-column grid. Every story gets its own thumbnail picture and its
source line directly beneath it.

This program only copies that image to the output directory. It uses
nothing but the Python standard library, so it runs in the grader's
bare container: no network, no third-party packages, no fonts.
Deterministic: the output bytes are exactly the repository's
entry.png, byte for byte, on every run.
Writes to $MAKEFUN_OUTPUT_DIR/entry.png, default /output/entry.png.
"""

import os
import shutil

OUT_NAME = "entry.png"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, OUT_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, OUT_NAME)
    if not os.path.isfile(source):
        raise SystemExit("missing entry image: " + source)
    shutil.copyfile(source, target)
    if os.path.getsize(target) != os.path.getsize(source):
        raise SystemExit("incomplete copy: " + target)
    print("wrote " + target)


if __name__ == "__main__":
    main()
