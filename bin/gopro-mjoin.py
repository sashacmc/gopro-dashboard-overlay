#!/usr/bin/env python3

import sys

from gopro_overlay.ffmpeg import FFMPEG
from gopro_overlay.ffmpeg_gopro import FFMPEGGoPro

if __name__ == "__main__":
    in_files = sys.argv[1:-1]
    output = sys.argv[-1]
    print("in:", in_files)
    print("out:", output)
    ffmpeg_gopro = FFMPEGGoPro(FFMPEG(None))
    ffmpeg_gopro.join_files(
        filepaths=in_files,
        output=output
    )
