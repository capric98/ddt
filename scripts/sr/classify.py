#!/usr/bin/env python3
# coding: utf-8
import argparse
import inspect
import os
import re
import shutil
import sys


def _create_on_not_exist(p):
    if not os.path.isdir(p):
        os.makedirs(p)

def init_output(op):
    _create_on_not_exist(os.path.join(op, "Rank"))
    _create_on_not_exist(os.path.join(op, "Avatar"))
    _create_on_not_exist(os.path.join(op, "GraffitTag"))
    _create_on_not_exist(os.path.join(op, "FaceMap"))
    _create_on_not_exist(os.path.join(op, "Sticker"))
    _create_on_not_exist(os.path.join(op, "GachaImg"))
    _create_on_not_exist(os.path.join(op, "Minimap"))


def _base_fn(fn):
    return os.path.split(fn)[-1]

def filter_Rank(fn, op):
    if re.search(r"\d{4}_Rank_\d{1}", _base_fn(fn)):
        shutil.copyfile(fn, os.path.join(op, "Rank", _base_fn(fn)))

def filter_Avatar(fn, op):
    if re.match(r"Avatar_", _base_fn(fn)):
        fns = _base_fn(fn).split("_")
        if not os.path.isdir(os.path.join(op, "Avatar", fns[1])):
            os.mkdir(os.path.join(op, "Avatar", fns[1]))
        shutil.copyfile(fn, os.path.join(op, "Avatar", fns[1], _base_fn(fn)))

def filter_GraffitTag(fn, op):
    if re.match(r"GraffitTag", _base_fn(fn)):
        shutil.copyfile(fn, os.path.join(op, "GraffitTag", _base_fn(fn)))

def filter_FaceMap(fn, op):
    if re.match(r"W_\d{3}", _base_fn(fn)):
        shutil.copyfile(fn, os.path.join(op, "FaceMap", _base_fn(fn)))
    if re.match(r"M_\d{3}", _base_fn(fn)):
        shutil.copyfile(fn, os.path.join(op, "FaceMap", _base_fn(fn)))

def filter_Sticker(fn, op):
    if re.match(r"\d{6}\.png", _base_fn(fn)):
        shutil.copyfile(fn, os.path.join(op, "Sticker", _base_fn(fn)))

def filter_Minimap(fn, op):
    if re.match(r"^Minimap_.*\.png", _base_fn(fn)):
        shutil.copyfile(fn, os.path.join(op, "Minimap", _base_fn(fn)))

def filter_GachaImg(fn, op):
    if re.match(r"GachaImg.*\.png", _base_fn(fn)):
        shutil.copyfile(fn, os.path.join(op, "GachaImg", _base_fn(fn)))

def filter_Chap(fn, op):
    if re.match(r"Chap(_?)\d{2}_", _base_fn(fn)): os.remove(fn)
def filter_NPC(fn, op):
    if re.match(r"^NPC_", _base_fn(fn)): os.remove(fn)
def filter_Monster(fn, op):
    if re.match(r"^Monster_", _base_fn(fn)): os.remove(fn)
def filter_Heliobus(fn, op): # 罗浮杂俎？
    if re.match(r"^Heliobus", _base_fn(fn)): os.remove(fn)
def filter_miscellaneous(fn, op):
    if re.match(r"^Metal", _base_fn(fn)): os.remove(fn)
    if re.match(r"^M_Chap", _base_fn(fn)): os.remove(fn)
    if re.match(r"^MeetMat", _base_fn(fn)): os.remove(fn)
    if re.match(r"^UI3D", _base_fn(fn)): os.remove(fn)
    if re.match(r"^UI_", _base_fn(fn)): os.remove(fn)
    if re.match(r"^Eff_", _base_fn(fn)): os.remove(fn)
    if re.match(r"^Objects_Chap", _base_fn(fn)): os.remove(fn)
    if re.match(r"^MaterialIDV", _base_fn(fn)): os.remove(fn)
    if re.match(r"^IRI_Line", _base_fn(fn)): os.remove(fn)
    if re.match(r"^IndStyle", _base_fn(fn)): os.remove(fn)
    if re.match(r"^Enviro_", _base_fn(fn)): os.remove(fn)
    if re.match(r"^Common_Game", _base_fn(fn)): os.remove(fn)
    if re.match(r"^Abyss_", _base_fn(fn)): os.remove(fn)


filters = [ obj for name,obj in inspect.getmembers(sys.modules[__name__]) if (inspect.isfunction(obj) and name.startswith("filter")) ]


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="input dir")
    parser.add_argument("-o", "--output", type=str, help="input dir")

    args = parser.parse_args()

    if not os.path.isdir(args.input):
        print(f"Input dir \"{args.input}\" does not exist!")
        exit(1)
    if not os.path.isdir(args.output):
        print(f"Output dir \"{args.output}\" does not exist!")
        exit(1)

    init_output(args.output)

    for root, _, files in os.walk(args.input):
        for fn in files:
            for func in filters:
                func(os.path.join(root, fn), args.output)