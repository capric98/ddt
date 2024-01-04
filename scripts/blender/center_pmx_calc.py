#!/usr/bin/env python3
# coding: utf-8

# Data from CopanoRickey fbx scale at 100.
uma_dx = 0
uma_dy = 0.023805 - 0.034437
uma_dz = 0.989637 - 0.908125

uma_center_z = 0.908125
uma_thigh = 0.352816
uma_leg   = 0.402078

_FIXED_FACTOR_ = None

def pos_to_tuple(pos):
    x, y, z = pos.split(" ")
    return (float(x), float(y), float(z))

if __name__ == "__main__":
    hip_x, hip_y, hip_z    = pos_to_tuple(input("足位置(空格隔开)："))
    knee_x, knee_y, knee_z = pos_to_tuple(input("ひざ位置(空格隔开)："))
    foot_x, foot_y, foot_z = pos_to_tuple(input("足首位置(空格隔开)："))

    thigh = ((hip_x-knee_x)**2 + (hip_y-knee_y)**2 + (hip_z-knee_z)**2) ** 0.5
    leg   = ((foot_x-knee_x)**2 + (foot_y-knee_y)**2 + (foot_z-knee_z)**2) ** 0.5

    mmd_factor = leg / uma_leg if not _FIXED_FACTOR_ else _FIXED_FACTOR_
    thigh_factor = thigh / uma_thigh

    print(f"scale factor: {mmd_factor:.2f}")
    print(f"thigh factor: {thigh_factor:.2f}")

    pos_y = uma_center_z * mmd_factor # see below

    offset_x = uma_dx * mmd_factor
    offset_y = uma_dz * mmd_factor # Blender coordinates -> PMX Editor coordinates
    offset_z = uma_dy * mmd_factor # Blender coordinates -> PMX Editor coordinates

    print(f"新的センター Position：0 {pos_y} {hip_z}")
    print(f"新的センター offset：{offset_x} {offset_y} {offset_z}")
