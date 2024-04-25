#!/usr/bin/env python3
# coding: utf-8

# Data from CopanoRickey fbx scale at 100.
uma_dx = 0
uma_dy = 0.048311 - 0.052331
uma_dz = 1.42208 - 1.36687
length = (uma_dx**2 + uma_dy**2 + uma_dz**2) ** 0.5


if __name__ == "__main__":
    head_offset = input("頭 offset(空格隔开): ")

    hx, hy, hz = head_offset.split(" ")
    hx, hy, hz = float(hx), float(hy), float(hz)

    length_head = (hx**2 + hy**2 + hz**2) ** 0.5

    offset_x = length_head*(uma_dx/length)
    offset_y = length_head*(uma_dz/length) # Blender coordinates -> PMX Editor coordinates
    offset_z = length_head*(uma_dy/length) # Blender coordinates -> PMX Editor coordinates

    print(f"新的頭 offset：{offset_x} {offset_y} {offset_z}")
