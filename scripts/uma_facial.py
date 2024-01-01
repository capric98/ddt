#!/usr/bin/env python3
# coding: utf-8
import requests, sys, time
from pathlib import Path
cwd = Path(__file__).resolve().parent
sys.path.append(str(cwd.parent))

from ddt.umamusume.camera import *

morph_dict = {
    "Mouth_1": "口角上げ",
    "Mouth_4": "口角上げ",
    "Mouth_5": [("お", 0.7), ("口角上げ", 0.8)],
    "Mouth_6": [("お", 0.7), ("口角上げ", 0.8)],
    "Mouth_7": [("お", 0.7), ("口角上げ", 0.8)],
    "Mouth_8": "い４",
    "Mouth_9": "口角下げ2",
    "Mouth_11": "倒ω",
    "Mouth_14": "お２",
    "Mouth_15": [("あ２", 0.8)],
    "Mouth_17": [("□２", 0.5)],
    "Mouth_23": [("あ", 0.5), ("口角上げ", 0.5)],
    "Mouth_24": [("お", 0.7), ("口角上げ", 0.8)],
    "Mouth_25": "い４",
    "Mouth_26": [("い４", 0.9),("口横広げ", 0.2)],
    "Mouth_27": [("う", 0.7), ("口角下げ", 0.2)],
    "Mouth_28": [("お", 0.7), ("口角下げ", 0.2)],
    "Mouth_29": [("お", 0.4), ("口角上げ", 0.3)],
    "Mouth_30": [("お", 0.5), ("口角上げ", 0.7)],
    "Mouth_31": [("お", 1.0)],
    "Mouth_32": [("お", 1.0), ("あ", 0.15), ("口横広げ", 0.1)],
    "Mouth_33": [("お", 0.5), ("口角下げ", 0.2)],
    "Mouth_34": [("お", 0.6), ("口横広げ", 0.3), ("口角下げ", 0.15)],
    "Mouth_35": [("い", 1.0), ("口上", 0.2)],
    "Mouth_36": [("い", 1.0), ("口上", 0.2)],
    "Mouth_37": [("え1", 0.5)],
    "Mouth_38": [("お", 0.5), ("口角下げ", 0.2), ("口横広げ", 0.1)],
    "Mouth_54": [("口横広げ", 0.3)],
    "Eye_1_L": [("ウィンク２", 0.4)],
    "Eye_1_R": [("ｳｨﾝｸ２右", 0.4)],
    "Eye_2_L": "ウィンク２",
    "Eye_2_R": "ｳｨﾝｸ２右",
    "Eye_3_L": [("ウィンク", 0.3)],
    "Eye_3_R": [("ウィンク右", 0.3)],
    "Eye_4_L": [("ウィンク", 0.5)],
    "Eye_4_R": [("ウィンク右", 0.5)],
    "Eye_5_L": [("ウィンク", 1.0)],
    "Eye_5_R": [("ウィンク右", 1.0)],
    "Eye_6_L": [("ウィンク２", 0.1)],
    "Eye_6_R": [("ｳｨﾝｸ２右", 0.1)],
    "Eye_7_L": [("ウィンク", 0.1)],
    "Eye_7_R": [("ウィンク右", 0.1)],
    "Eye_8_L": [("ウィンク", 1)],
    "Eye_8_R": [("ウィンク右", 1)],
    "Eye_9_L": [("ウィンク２", 0.05)],
    "Eye_9_R": [("ｳｨﾝｸ２右", 0.05)],
    "Eye_10_L": [("ウィンク２", 0.05)],
    "Eye_10_R": [("ｳｨﾝｸ２右", 0.05)],
    "Eye_11_L": [("ウィンク２", 0.08)],
    "Eye_11_R": [("ｳｨﾝｸ２右", 0.08)],
    "Eye_12_L": [("びっくり1", 0.3)],
    "Eye_13_L": [("瞳小", 0.8)],
    "Eye_14_L": [("瞳小", 0.8)],
    "Eye_15_L": [("なごみ左", 0.2)],
    "Eye_15_R": [("なごみ右", 0.2)],
    "Eye_16_L": "なごみ左",
    "Eye_16_R": "なごみ右",
    "Eye_17_L": [("ウィンク２", 0.2)],
    "Eye_17_R": [("ｳｨﾝｸ２右", 0.2)],
    "Eye_18_L": [("ウィンク", 0.1)],
    "Eye_18_R": [("ウィンク右", 0.1)],
    "Eye_23_L": [("ウィンク２", 0.15)],
    "Eye_23_R": [("ｳｨﾝｸ２右", 0.15)],
    "Ebrow_1_L": [("上", 0.2)],
    "Ebrow_2_L": [("下", 0.2)],
    "Ebrow_3_L": [("下", 0.8)],
    "Ebrow_4_L": "下",
    "Ebrow_5_L": "怒り",
    "Ebrow_6_L": "困る",
    "Ebrow_7_L": "怒り",
    "Ebrow_8_L": "にこり",
    "Ebrow_9_L": [("上", 0.3)],
    "Ebrow_11_L": "下",
    "Ebrow_13_L": "困る",
    "Ebrow_14_L": "下",
    "Ebrow_15_L": "怒り",
    "Ebrow_16_L": "怒り",
    "Ebrow_17_L": [("怒り", 1.0), ("にこり", 0.5)],
    "Ebrow_19_L": [("怒り", 1.0), ("にこり", 0.5)],
    "Ebrow_20_L": "困る",
    "Ebrow_21_L": "上",
    "Ebrow_22_L": "下",
}
skip_list = [
    "Eye_12_R",
    "Eye_13_R",
    "Eye_14_R",
    "Eye_19_L",
    "Eye_19_R",
    "Mouth_42",
    "Mouth_52",
    "Mouth_53",
    "Ebrow_12_L"
]

def camera_to_txt(id: int, fn, out: str, morph_dict=morph_dict, skip_list=skip_list) -> list[str]:

    shape_keys = parse_facial(fn, chara_id=id, map=morph_dict)

    unresolved = []
    for v in shape_keys:
        if "_" in v.name:
            if v.name.startswith("Ebrow") and v.name.endswith("R"): continue
            if v.name in skip_list: continue
            if v.name not in unresolved:
                unresolved.append(v.name)
    # unresolved.sort()
    # if unresolved: print("Unresolved Morph Keys:")
    # for v in unresolved:
    #     print(f"  {v}")

    with open(out, "w", encoding="utf-8") as f:
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

    return unresolved


if __name__=="__main__":
    camera_fn = "son10xx_camera"

    unresolved = []
    unresolved += camera_to_txt(1, camera_fn, "1st.txt")
    unresolved += camera_to_txt(2, camera_fn, "2nd.txt")
    unresolved += camera_to_txt(3, camera_fn, "3rd.txt")

    unresolved = list(dict.fromkeys(unresolved))
    unresolved.sort()
    if unresolved: print("Unresolved Morph Keys:")
    for v in unresolved:
        print(f"  {v}")