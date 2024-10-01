#!/usr/bin/env python3
# coding: utf-8
import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

__PYTHON__ = shutil.which("python3") if shutil.which("python3") else shutil.which("python")
__SCRIPT__ = os.path.join(Path(__file__).resolve().parent, "make_ik_from_vmd.py")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="batch_ik.py")
    parser.add_argument("--uma", type=str, help="Uma PMX model", required=True)
    parser.add_argument("--mmd", type=str, help="MMD PMX model", required=True)
    parser.add_argument("--vmd", type=str, help="VMD Directory", required=True)

    args = parser.parse_args()

    uma_pmx = args.uma
    mmd_pmx = args.mmd
    vmd_dir = args.vmd

    for f in os.listdir(vmd_dir):
        if f.lower().endswith(".vmd"):
            fn = os.path.join(vmd_dir, f)
            fargs = [
                __PYTHON__, __SCRIPT__,
                "--source", os.path.abspath(uma_pmx),
                "--target", os.path.abspath(mmd_pmx),
                "--motion", os.path.abspath(fn),
            ]

            # for fa in fargs:
            #     if fa.startswith("--") or fa.lower().endswith(".exe"):
            #         print(fa, end=" ")
            #     else:
            #         print(f"\"{fa}\"", end=" ")
            # print()

            subprocess.run(fargs, stdout=sys.stdout, stderr=sys.stderr)
            print("==================================================")
            time.sleep(3)