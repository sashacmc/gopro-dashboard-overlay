#!/usr/bin/python3

import os
import shutil
import argparse
import subprocess
import tempfile

import mixvideoconcat


def call_gopro_dashboard(layout, gpx, infile, outfile):
    command = [
        "gopro-dashboard.py",
        "--units-speed",
        "kph",
        "--gps-speed-max",
        "300",
        "--layout",
        "xml",
        "--layout-xml",
        layout,
    ]

    if gpx is not None:
        command += [
            "--full-timeseries-journey",
            "--use-gpx-only",
            "--video-time-start",
            "mp4-created",
            "--gpx",
            gpx,
        ]

    command.append(infile)
    command.append(outfile)

    print(f"run: {command}")
    subprocess.run(command)


def join_files(layout, gpx, infiles, outfile):
    if len(infiles) == 0:
        return
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpfiles = []
        for i, f in enumerate(infiles):
            tfile = os.path.join(tmpdir, f"{i}_dash.mp4")
            call_gopro_dashboard(layout, gpx, f, tfile)
            if not os.path.exists(tfile):
                raise UserWarning("Conversion error")
            tmpfiles.append(tfile)

        if len(tmpfiles) == 1:
            shutil.copyfile(tmpfiles[0], outfile)
        else:
            mixvideoconcat.concat(
                tmpfiles,
                outfile,
                tmpdir,
                deinterlace_mode=False,
                stabilize_mode=False,
            )


def __args_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("infiles", nargs="+", help="Files to process")
    parser.add_argument("outfile", help="Out file")
    parser.add_argument("--layout", help="layout", default=None)
    parser.add_argument("--gpx", help="", default=None)
    return parser.parse_args()


if __name__ == "__main__":
    args = __args_parse()

    join_files(args.layout, args.gpx, args.infiles, args.outfile)
