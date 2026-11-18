#!/usr/bin/env python3
"""News-image entry for Tuesday 17 November 2026 (make.fun program/v1).

Standard library only. The entry image — a one-page newspaper front page
summing up the day's world news — is entry.png beside this file, drawn at
build time by generate.py. This program copies it to /output/entry.png,
exactly as the competition rules allow ("a repository holding the image and
a one-line program that copies it there; a program may also draw it").

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    src = Path(__file__).resolve().parent / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / "entry.png")


if __name__ == "__main__":
    main()
