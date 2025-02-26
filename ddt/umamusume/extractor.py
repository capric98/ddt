def __mstime_to_str(t: int) -> str:
    ms = t % 1000
    seconds = t//1000
    min = t//(1000*60)
    hour = t//(1000*60*60)
    seconds = seconds - min*60
    min = min - hour*60
    return "{:02d}:{:02d}:{:02d},{:03d}".format(hour, min, seconds, ms)


def lyrics_to_srt(input, output):

    import UnityPy
    import requests

    count = 0
    last_lyric = ""

    with open(output, "w", encoding="utf-8") as f:

        translation = []
        try:
            tjson = requests.get("https://raw.githubusercontent.com/MinamiChiwa/Trainers-Legend-G-TRANS/master/localized_data/LIVE.json", timeout=10).json()
            for (_, v) in tjson.items():
                v = v.strip()
                if v: translation.append(v)
        except:
            pass
        else:
            count += 1
            print("1", file=f)
            print("00:00:00,000 --> 00:00:02,000", file=f)
            print("翻译：\n", file=f)

        for _, v in UnityPy.load(input).container.items():
            if v.type.name == "TextAsset":

                # try:
                #     vs = bytes(v.read().script).decode("utf-8")
                # except Exception as _:
                #     vs = v.read().m_Script

                for line in v.read().m_Script.splitlines():
                    content = line.strip().split(",")
                    if not content[0].isnumeric(): continue

                    lyric = "".join(content[1:])
                    lyric = lyric.strip()

                    if lyric:
                        for t in translation:
                            if t.startswith(lyric):
                                lyric = t

                    if last_lyric:
                        print("{}".format(__mstime_to_str(int(content[0])-1)), file=f)
                        print(last_lyric, file=f, end="\n\n")

                    if lyric:
                        count +=1
                        print(f"{count}", file=f)
                        print("{} -->".format(__mstime_to_str(int(content[0]))), file=f, end=" ")

                    last_lyric = lyric

        if last_lyric:
            print("{}".format(__mstime_to_str(int(content[0]))), file=f)
            print(last_lyric, file=f)



def __parse_motion(fn):
    import UnityPy

    rotation_curves = []
    position_curves = []
    scale_curves = []

    for f in fn:
        for obj in UnityPy.load(f).objects:
            # print(obj.type.name)
            if obj.type.name=="AnimationClip":
                clip = obj.read()
                break

        # print("================================================")
        # print("====================Rotation====================")


        for v in clip.m_RotationCurves:
            # print(v.path, len(v.curve.m_Curve))
            # if v.path not in path_list: path_list.append(v.path)
            m_Curve = []
            for crv in v.curve.m_Curve:
                # print(crv)
                # print(crv.time) # The time of the keyframe.
                # print(crv.value.X, crv.value.Y, crv.value.Z, crv.value.W)
                # print(crv.inSlope.X, crv.inSlope.Y, crv.inSlope.Z, crv.inSlope.W)
                # print(crv.outSlope.X, crv.outSlope.Y, crv.outSlope.Z, crv.outSlope.W)
                # print(crv.weightedMode) # https://docs.unity3d.com/ScriptReference/WeightedMode.html
                # print(crv.inWeight.X, crv.inWeight.Y, crv.inWeight.Z, crv.inWeight.W)
                # print(crv.outWeight.X, crv.outWeight.Y, crv.outWeight.Z, crv.outWeight.W)
                m_Curve.append({
                    "time": crv.time,
                    "value": {"X": crv.value.X, "Y": crv.value.Y, "Z": crv.value.Z, "W": crv.value.W},
                    "inSlope": {"X": crv.inSlope.X, "Y": crv.inSlope.Y, "Z": crv.inSlope.Z, "W": crv.inSlope.W},
                    "outSlope": {"X": crv.outSlope.X, "Y": crv.outSlope.Y, "Z": crv.outSlope.Z, "W": crv.outSlope.W},
                })
                # break
            # break
            rotation_curves.append({"path": v.path, "m_Curve": m_Curve})

        # print("====================Position====================")

        for v in clip.m_PositionCurves:
            # print(v.path, len(v.curve.m_Curve))
            # if v.path not in path_list: path_list.append(v.path)
            m_Curve = []
            for crv in v.curve.m_Curve:
                # print(crv.value.X, crv.value.Y, crv.value.Z)
                # print(crv.inSlope.X, crv.inSlope.Y, crv.inSlope.Z)
                # print(crv.outSlope.X, crv.outSlope.Y, crv.outSlope.Z)
                m_Curve.append({
                    "time": crv.time,
                    "value": {"X": crv.value.X, "Y": crv.value.Y, "Z": crv.value.Z},
                    "inSlope": {"X": crv.inSlope.X, "Y": crv.inSlope.Y, "Z": crv.inSlope.Z},
                    "outSlope": {"X": crv.outSlope.X, "Y": crv.outSlope.Y, "Z": crv.outSlope.Z},
                })
                # break
            position_curves.append({"path": v.path, "m_Curve": m_Curve})

        for v in clip.m_ScaleCurves: # ???
            # print(v.path, len(v.curve.m_Curve))
            # if v.path not in path_list: path_list.append(v.path)
            m_Curve = []
            for crv in v.curve.m_Curve:
                # print(crv.value.X, crv.value.Y, crv.value.Z)
                # print(crv.inSlope.X, crv.inSlope.Y, crv.inSlope.Z)
                # print(crv.outSlope.X, crv.outSlope.Y, crv.outSlope.Z)
                m_Curve.append({
                    "time": crv.time,
                    "value": {"X": crv.value.X, "Y": crv.value.Y, "Z": crv.value.Z},
                    "inSlope": {"X": crv.inSlope.X, "Y": crv.inSlope.Y, "Z": crv.inSlope.Z},
                    "outSlope": {"X": crv.outSlope.X, "Y": crv.outSlope.Y, "Z": crv.outSlope.Z},
                })
                # break
            scale_curves.append({"path": v.path, "m_Curve": m_Curve})

    return {
        "m_RotationCurves": rotation_curves,
        "m_PositionCurves": position_curves,
        "m_ScaleCurves": scale_curves,
    }

def motion_to_json(fn, output, indent=None):
    import json
    with open(output, "w") as f:
        if isinstance(fn, list):
            json.dump(__parse_motion(fn), fp=f, indent=indent)
        else:
            json.dump(__parse_motion([fn]), fp=f, indent=indent)