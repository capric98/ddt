#!/usr/bin/env python3
# coding: utf-8
import sys, time
from pathlib import Path
cwd = Path(__file__).resolve().parent
sys.path.append(str(cwd.parent))

from ddt.translator import Caiyun


if __name__=="__main__":
    client = Caiyun(input("token: "))
    file   = input("file path: ")

    with open(file, "r", encoding="utf-8") as f:
        with open(".zh.".join(file.rsplit(".", 1)), "w", encoding="utf-8") as of:
            for line in f:
                start  = time.time()
                line   = line.strip()
                interp = client.interp(line)
                end    = time.time()
                print("[{:.2f}]".format(end-start), f"{line} -> {interp}")
                print(interp, file=of, flush=True)