#!/usr/bin/env python3
from math import log10

from pydub import AudioSegment
from UnityPy import load as unity_load


__BGM__ = [] # filenames
__VOC__ = [] # filenames

__CAMERA__ = "" # filename
__OUTPUT__ = "" # filename

singer_num = len(__VOC__)


def contain_id(id: int, mask: int) -> bool:
    # (262143)D = (111111111111111111)B
    return (mask >> id) % 2 == 1

def calc_gain(num: int, total: int=singer_num) -> float:
    return 10 * log10(total/num)

def mix_segment(keyframe, vocal: list[AudioSegment], ltime: int, rtime: int) -> tuple[list[AudioSegment], int]:
    cnt = 0
    seg = None

    for id in range(singer_num):
        if ("character" in keyframe) and (not contain_id(id, keyframe["character"])): continue
        cnt += 1

        temp = vocal[id][ltime:rtime]
        seg  = temp if not seg else seg.overlay(temp)

    return seg, cnt


if __name__=="__main__":

    mix = None

    for fn in __BGM__:
        audio = AudioSegment.from_file(fn)
        mix   = audio if not mix else mix.overlay(audio)

    vocal = [AudioSegment.from_file(fn) for fn in __VOC__]


    for obj in unity_load(__CAMERA__).objects:
        if obj.type.name == "MonoBehaviour":
            if obj.serialized_type.nodes:
                tree = obj.read_typetree()


    ltime = 0
    for v in tree["ripSyncKeys"]["thisList"]:
        time = v["frame"] * 1000 // 60

        if ltime>=time:
            last_v = v
            continue

        seg, cnt = mix_segment(last_v, vocal, ltime, time)

        if cnt>0:
            # print(ltime, time)
            mix = mix.overlay(
                seg.apply_gain(calc_gain(cnt)),
                position = ltime,
            )

        ltime  = time
        last_v = v

    # handle the last part
    seg, cnt = mix_segment(last_v, vocal, ltime, -1)

    if cnt>0:
        # print(ltime, time)
        mix = mix.overlay(
            seg.apply_gain(calc_gain(cnt)),
            position = ltime,
        )

    mix.export(__OUTPUT__, format=__OUTPUT__.split(".")[-1])
    # # If you need 24bits output...
    # mix.export(
    #     __OUTPUT__,
    #     format=__OUTPUT__.split(".")[-1],
    #     parameters=["-c:a", "pcm_s24le"],
    # )