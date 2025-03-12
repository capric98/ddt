#!/usr/bin/env python
# coding: utf-8

uma_thigh = 0.352816
uma_leg   = 0.402078
# uma_l2f   = 0.48754

uma_pos = [0, 11.35156, 0.4304609]
uma_off = [0, 1.018911, -0.1329028]

if __name__ == "__main__":
    mmd_thigh = float(input("请输入模型大腿长度：").strip())
    mmd_leg = float(input("请输入模型小腿长度：").strip())
    # mmd_l2f = float(input("请输入模型膝关节到脚腹长度：").strip())

    if mmd_thigh > 5: mmd_thigh = mmd_thigh * 0.08
    if mmd_leg > 5: mmd_leg = mmd_leg * 0.08
    # if mmd_l2f > 5: mmd_leg = mmd_leg * 0.08

    ratio_t = mmd_thigh / uma_thigh
    ratio_l = mmd_leg / uma_leg
    ratio   = (ratio_l + ratio_t) / 2

    print(f"大腿缩放比例：{ratio_t}")
    print(f"小腿缩放比例：{ratio_l}")
    print(f"平均缩放比例：{ratio}")

    # print("大腿缩放比例下的センター骨：")
    # print(f"  Position: {[v*ratio_t for v in uma_pos]}")
    # print(f"  offset:   {[v*ratio_t for v in uma_off]}")

    # print("小腿缩放比例下的センター骨：")
    # print(f"  Position: {[v*ratio_l for v in uma_pos]}")
    # print(f"  offset:   {[v*ratio_l for v in uma_off]}")

    print("平均缩放比例下的センター骨：")
    print(f"  Position: {[v*ratio for v in uma_pos]}")
    print(f"  offset:   {[v*ratio for v in uma_off]}")
