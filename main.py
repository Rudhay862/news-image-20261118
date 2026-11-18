#!/usr/bin/env python3
"""Write the 18 November 2026 world-news image to /output/entry.png.

The image is bundled in this repository as entry.png; this program
copies it to the output directory deterministically, with no network.
Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output.
"""
import hashlib
import os
import shutil
import sys

SRC_NAME = "entry.png"
# SHA-256 of the bundled entry.png; the copy is refused if it differs.
EXPECTED_SHA256 = "b3bb6f2f8bedead5e6c89e00d052ca4ffbe011b745e96bd5a0f85ddc3cc72ebc"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    with open(src, "rb") as f:
        data = f.read()
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        sys.exit("entry.png sha256 mismatch; refusing to write output")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    # Clear the output directory's contents only; never remove the
    # directory itself (the grader user cannot recreate it).
    for name in os.listdir(out_dir):
        path = os.path.join(out_dir, name)
        if os.path.isfile(path) or os.path.islink(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
    with open(os.path.join(out_dir, SRC_NAME), "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
