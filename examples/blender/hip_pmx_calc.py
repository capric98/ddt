#!/usr/bin/env python3
# coding: utf-8

# Data from CopanoRickey fbx scale at 100.
uma_dx = 0
uma_dy = 0.023805 - 0.034437
uma_dz = 0.989637 - 0.908125

uma_shift_z = 0.908125 - 0.881235
uma_thigh_height = 0.881235

if __name__ == "__main__":
    right_thigh = input("右足位置(空格隔开)：")
    left_thigh  = input("左足位置(空格隔开)：")

    rx, ry, rz = right_thigh.split(" ")
    lx, ly, lz = left_thigh.split(" ")

    rx, ry, rz = float(rx), float(ry), float(rz)
    lx, ly, lz = float(lx), float(ly), float(lz)

    thigh_height = (ly+ry) / 2 # ly与ry应该相同，以防万一

    print(f"\n你输入的右足位置：{rx} {ry} {rz}")
    print(f"你输入的左足位置：{lx} {ly} {lz}\n")

    mmd_factor = thigh_height / uma_thigh_height

    pos_x = (lx+rx) / 2
    pos_y = thigh_height + uma_shift_z * mmd_factor # see below
    pos_z = (lz+rz) / 2

    offset_x = uma_dx * mmd_factor
    offset_y = uma_dz * mmd_factor # Blender coordinates -> PMX Editor coordinates
    offset_z = uma_dy * mmd_factor # Blender coordinates -> PMX Editor coordinates

    print(f"新的下半身 Position：{pos_x} {pos_y} {pos_z}")
    print(f"新的下半身 offset：{offset_x} {offset_y} {offset_z}")
