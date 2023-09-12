#!/usr/bin/env python3
# coding: utf-8
import os
import shutil
import subprocess
import tempfile
from math import log10

from pydub import AudioSegment
from UnityPy import load as unity_load


__BGM__ = [] # awb filenames
__VOC__ = [] # awb filenames

__CAMERA__ = "" # filename
__OUTPUT__ = "" # filename


__VGMEXE__ = shutil.which("vgmstream-cli")
if not __VGMEXE__:
    print("vgmsteam-cli not found, please install it and add it to PATH.")
    exit(1)


def contain_id(id: int, mask: int) -> bool:
    # (262143)D = (111111111111111111)B
    return (mask >> id) % 2 == 1


def calc_gain(num: int, total: int) -> float:
    return 10 * log10(total/num)


def mix_segment(keyframe, vocal: list[AudioSegment], ltime: int, rtime: int, stream: int) -> tuple[list[AudioSegment], int]:
    cnt = 0
    seg = None

    for id in range(len(vocal)):
        if ("character" in keyframe) and (not contain_id(id, keyframe["character"])): continue
        if stream>=len(vocal[id]): continue
        cnt += 1

        temp = vocal[id][stream][ltime:rtime]
        seg  = temp if not seg else seg.overlay(temp)

    return seg, cnt


def mix_keylist(mix: AudioSegment, vocal: list[list[AudioSegment]], tree: dict, stream: int, _callback=None) -> AudioSegment:
    vocal_num = len(vocal)
    ltime = 0
    for v in tree:
        time = v["frame"] * 1000 // 60

        if ltime>=time:
            last_v = v
            continue

        seg, cnt = mix_segment(last_v, vocal, ltime, time, stream)

        if cnt>0:
            # print(ltime, time)
            mix = mix.overlay(
                seg.apply_gain(calc_gain(cnt, vocal_num)),
                position = ltime,
            )

        ltime  = time
        last_v = v

        if _callback: _callback()

    # handle the last part
    seg, cnt = mix_segment(last_v, vocal, ltime, -1, stream)

    if cnt>0:
        # print(ltime, time)
        mix = mix.overlay(
            seg.apply_gain(calc_gain(cnt, vocal_num)),
            position = ltime,
        )
        if _callback: _callback()

    return mix


def load_awb(awb_fn: str) -> list[AudioSegment]:
    temp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
    subprocess.run([__VGMEXE__, "-F", "-l", "1", "-S", "0", "-o", os.path.join(temp.name, f"{awb_fn}.?s.wav"), awb_fn], capture_output=True)

    def get_stream_num(fn: str) -> int:
        stream_num = int(fn.split(".")[-2])
        return stream_num


    stream_list = os.listdir(temp.name)
    stream_list.sort(key=get_stream_num)
    stream_list = [os.path.join(temp.name, v) for v in stream_list]

    audio_list = load_wav(stream_list)

    temp.cleanup()

    return audio_list


def load_wav(stream_list: list[str]) -> list[AudioSegment]:
    audio_list  = []

    for fn in stream_list:
        if fn.endswith("wav"):
            audio_list.append(AudioSegment.from_file(fn))

    return audio_list


def load_voc(fn: str | list[str]) -> list[AudioSegment]:
    if isinstance(fn, list):
        return load_wav(fn)
    else:
        if fn.endswith(".wav"):
            return load_wav([fn])
        else:
            return load_awb(fn)


if __name__=="__main__":

    mix = None

    for fn in __BGM__:
        audio_list = load_awb(fn)
        for audio in audio_list:
            mix = audio if not mix else mix.overlay(audio)
    print("BGM loaded...")

    vocal = [load_voc(fn) for fn in __VOC__]
    print(f"{len(vocal)} vocal loaded...")


    for obj in unity_load(__CAMERA__).objects:
        if obj.type.name == "MonoBehaviour":
            if obj.serialized_type.nodes:
                tree = obj.read_typetree()

    total = 0;
    if "ripSyncKeys" in tree and "thisList" in tree["ripSyncKeys"]: total += len(tree["ripSyncKeys"]["thisList"])
    if "ripSync2Keys" in tree and "thisList" in tree["ripSync2Keys"]: total += len(tree["ripSync2Keys"]["thisList"])
    print(f"processing {total} segments...")


    if "ripSyncKeys" in tree and "thisList" in tree["ripSyncKeys"]: mix = mix_keylist(mix, vocal, tree["ripSyncKeys"]["thisList"], 0, lambda:print(">", end="", flush=True))
    if "ripSync2Keys" in tree and "thisList" in tree["ripSync2Keys"]: mix = mix_keylist(mix, vocal, tree["ripSync2Keys"]["thisList"], 1, lambda:print(">", end="", flush=True))


    mix.export(__OUTPUT__, format=__OUTPUT__.split(".")[-1])
    # # If you need 24bits output...
    # mix.export(
    #     __OUTPUT__,
    #     format=__OUTPUT__.split(".")[-1],
    #     parameters=["-c:a", "pcm_s24le"],
    # )

    print(f"\nexported to {__OUTPUT__}...")