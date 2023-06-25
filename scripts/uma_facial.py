#!/usr/bin/env python3
# coding: utf-8
import requests, sys, time
from pathlib import Path
cwd = Path(__file__).resolve().parent
sys.path.append(str(cwd.parent))

from ddt.umamusume.camera import *

morph_dict = {
    "Mouth_4": "口角上げ",
    "Mouth_6": "ワ1",
    "Mouth_8": [("い４", 1.0), ("口角上げ", 0.5)],
    "Mouth_9": [("口角下げ1", 1.0), ("口横縮げ", 0.4)],
    "Mouth_14": "あ", # ?
    "Mouth_28": "お1",
    "Mouth_29": [("ワ", 0.25)],
    "Eye_2_L": "ウィンク２",
    "Eye_2_R": "ｳｨﾝｸ２右",
    "Eye_3_L": [("ウィンク", 0.3)],
    "Eye_3_R": [("ウィンク右", 0.3)],
    "Eye_4_L": [("ウィンク", 0.5)],
    "Eye_4_R": [("ウィンク右", 0.5)],
    "Eye_7_L": [("ウィンク", 0.1)],
    "Eye_7_R": [("ウィンク右", 0.1)],
    "Eye_9_L": [("ウィンク２", 0.05)],
    "Eye_9_R": [("ｳｨﾝｸ２右", 0.05)],
    "Eye_12_L": [("びっくり1", 0.3)],
    # "Eye_12_R"
    "Eye_14_L": [("瞳小", 0.8)],
    # "Eye_14_R"
    "Eye_18_L": [("ウィンク", 0.1)],
    "Eye_18_R": [("ウィンク右", 0.1)],
    # "Eye_19_L"
    # "Eye_19_R"
    "Ebrow_5_L": "怒り",
    "Ebrow_9_L": [("上", 0.3)],
    "Ebrow_15_L": "怒り",
    "Ebrow_17_L": [("怒り", 1.0), ("にこり", 0.5)],
    "Ebrow_19_L": [("怒り", 1.0), ("にこり", 0.5)],
    "Ebrow_21_L": "上",
    "Ebrow_22_L": "下",
}

if __name__=="__main__":
    camera_fn = "son1080_camera"
    # for frame in parse_facial(camera_fn, chara_id=1):
    #     print(frame)
    shape_keys = parse_facial(camera_fn, chara_id=1)
    for v in unused_shape_key(shape_keys, morph_dict):
        print(v)

    shape_keys = to_mmd_shape_key(shape_keys, morph_dict)

    with open("output.txt", "w", encoding="utf-8") as f:
        num = len(shape_keys)
        f.write("version:,2\n")
        f.write("modelname:,Umamusume\n")
        f.write("boneframe_ct:,0\n")
        f.write("morphframe_ct:,"+str(num)+"\n")
        f.write("morph_name,frame_num,value\n")
        for k in shape_keys:
            # k.name = k.name.encode("utf-8").decode("shift-jis", "replace")
            f.write(f"{k.name},{k.frame},{k.weight}\n")
        f.write("camframe_ct:,0\n")
        f.write("lightframe_ct:,0\n")
        f.write("shadowframe_ct:,0\n")
        f.write("ik/dispframe_ct:,0\n")