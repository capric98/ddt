#!/usr/bin/env python3
# coding: utf-8
import sys, time
from pathlib import Path
cwd = Path(__file__).resolve().parent
sys.path.append(str(cwd.parent))

from ddt.umamusume import get_live_list

if __name__=="__main__":
    print(get_live_list()[0].assets)