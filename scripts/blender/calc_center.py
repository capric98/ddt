#!/usr/bin/env python3
# coding: utf-8

uma_center_pos = (0, 11.35156, 0.43046)

def pos_to_tuple(pos):
    x, y, z = pos.split(" ")
    return (float(x), float(y), float(z))

if __name__=="__main__":
    pos_x, pos_y, pos_z = pos_to_tuple(input("全亲位置(空格隔开)："))

    print(f"センター Position：{pos_x+uma_center_pos[0]} {pos_y+uma_center_pos[1]} {pos_z+uma_center_pos[2]}")
    print(f"センター offset：0 1 0")