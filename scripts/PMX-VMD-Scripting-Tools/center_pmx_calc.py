#!/usr/bin/env python3
# coding: utf-8

# Data from CopanoRickey fbx scale at 100.
# uma_dx = 0
# uma_dy = 0.023805 - 0.034437
# uma_dz = 0.989637 - 0.908125

uma_center_z = 0.908125
uma_thigh = 0.352816
uma_leg   = 0.402078

uma_center_pos = (0, 11.35156, 0.4304609)
uma_center_off = (0, 1.018911, -0.1329028)

_FIXED_FACTOR_ = None

def pos_to_tuple(pos):
    x, y, z = pos.split(" ")
    return (float(x), float(y), float(z))

if __name__ == "__main__":
    if not _FIXED_FACTOR_:
        hip_x, hip_y, hip_z    = pos_to_tuple(input("足位置(空格隔开)："))
        knee_x, knee_y, knee_z = pos_to_tuple(input("ひざ位置(空格隔开)："))
        foot_x, foot_y, foot_z = pos_to_tuple(input("足首位置(空格隔开)："))

        thigh = ((hip_x-knee_x)**2 + (hip_y-knee_y)**2 + (hip_z-knee_z)**2) ** 0.5
        leg   = ((foot_x-knee_x)**2 + (foot_y-knee_y)**2 + (foot_z-knee_z)**2) ** 0.5

        mmd_factor = leg / uma_leg
        thigh_factor = thigh / uma_thigh

        print(f"leg factor: {mmd_factor:.2f}")
        print(f"thigh factor: {thigh_factor:.2f}")

        mmd_factor = (leg+thigh)/(uma_leg+uma_thigh)
        print(f"\nscale factor: {mmd_factor:.2f}")
    else:
        mmd_factor = _FIXED_FACTOR_
        print(f"fixed factor: {mmd_factor:.2f}")


    mmd_factor /= 12.5

    pos_x = uma_center_pos[0] * mmd_factor
    pos_y = uma_center_pos[1] * mmd_factor # see below
    pos_z = uma_center_pos[2] * mmd_factor

    offset_x = uma_center_off[0] * mmd_factor
    offset_y = uma_center_off[1] * mmd_factor
    offset_z = uma_center_off[2] * mmd_factor

    print(f"新的センター Position：{pos_x} {pos_y} {pos_z}")
    print(f"新的センター offset：{offset_x} {offset_y} {offset_z}")
