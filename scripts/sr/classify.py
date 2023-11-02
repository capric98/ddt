#!/usr/bin/env python3
# coding: utf-8
import os
import argparse
import re
import shutil


def _create_on_not_exist(p):
    if not os.path.isdir(p):
        os.makedirs(p)

def init_output(op):
    _create_on_not_exist(os.path.join(op, "Rank"))
    _create_on_not_exist(os.path.join(op, "Avatar"))
    _create_on_not_exist(os.path.join(op, "GraffitTag"))
    _create_on_not_exist(os.path.join(op, "FaceMap"))
    _create_on_not_exist(os.path.join(op, "Sticker"))


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

def filter_Sticker(fn, op):
    if re.match(r"\d{6}.png", _base_fn(fn)):
        shutil.copyfile(fn, os.path.join(op, "Sticker", _base_fn(fn)))


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
    filters = [
        filter_Rank,
        filter_Avatar,
        filter_GraffitTag,
        filter_FaceMap,
        filter_Sticker,
    ]
    for root, _, files in os.walk(args.input):
        for fn in files:
            for func in filters:
                func(os.path.join(root, fn), args.output)