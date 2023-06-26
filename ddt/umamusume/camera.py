from dataclasses import dataclass


@dataclass
class MorphFrame:
    name: str
    frame: int
    weight: float


def contain_id(id: int, mask: int) -> bool:
    # (262143)D = (111111111111111111)B
    return (mask >> (id-1)) % 2 == 1

# Deprecated
def to_mmd_shape_key(keyframes: MorphFrame | list[MorphFrame], map: dict) -> list[MorphFrame]:
    if not isinstance(keyframes, list): keyframes = [keyframes]
    mmd_keyframes = []

    for kf in keyframes:
        if kf.name not in map:
            # mmd_keyframes.append(kf)
            continue
        else:
            mv = map[kf.name]
            if isinstance(mv, str): mv = [mv]

            for v in mv:
                if isinstance(v, str):
                    mmd_keyframes.append(MorphFrame(
                        name   = v,
                        frame  = kf.frame,
                        weight = 1.0*kf.weight,
                    ))
                else:
                    mmd_keyframes.append(MorphFrame(
                        name   = v[0],
                        frame  = kf.frame,
                        weight = v[1]*kf.weight,
                    ))

    mmd_keyframes.sort(key=lambda x: f"{x.frame:05d}_{x.name}")

    return mmd_keyframes

def unused_shape_key(keyframes: MorphFrame | list[MorphFrame], map: dict) -> list[str]:
    if not isinstance(keyframes, list): keyframes = [keyframes]
    unused = []

    for kf in keyframes:
        if kf.name not in map and kf.name not in unused:
            unused.append(kf.name)
    return unused

def _time_to_frame(time):
    return round(time*0.01 / (1/60))

def parse_facial(camera_fn, chara_id, map={}) -> list[MorphFrame]:
    import UnityPy

    for k, v in map.items():
        if isinstance(v, str):
            map[k] = [(v, 1.0)]

    for obj in UnityPy.load(camera_fn).objects:
        if obj.type.name == "MonoBehaviour":
            # export
            if obj.serialized_type.nodes:
                # save decoded data
                tree = obj.read_typetree()
                # fp = os.path.join(extract_dir, f"{tree['m_Name']}.json")
                # with open(fp, "wt", encoding = "utf8") as f:
                #     json.dump(tree, f, ensure_ascii = False, indent = 4)
            else:
                # save raw relevant data (without Unity MonoBehaviour header)
                # data = obj.read()
                # fp = os.path.join(extract_dir, f"{data.name}.bin")
                # with open(fp, "wb") as f:
                #     f.write(data.raw_data)
                pass

    data = tree["facial1Set"] if chara_id==1 else tree["other4FacialArray"][chara_id-2]

    if "ripSyncKeys" in tree and "thisList" in tree["ripSyncKeys"]:
        for v in tree["ripSyncKeys"]["thisList"]:
            if ("character" not in v) or (contain_id(chara_id, v["character"])):
                data["mouthKeys"]["thisList"].append(v)
        data["mouthKeys"]["thisList"].sort(key=lambda x: x["frame"])

    raw_data = data
    raw_data["ebrowKeys"] = raw_data["eyebrowKeys"]

    result = []

    for prefix in ["Mouth", "Eye", "Ebrow"]:
        data = raw_data[f"{prefix.lower()}Keys"]["thisList"]
        all_current = {
            "facialPartsDataArray": {},
            "facialPartsDataArrayL": {},
            "facialPartsDataArrayR": {},
        }

        for keyframe in data:
            frame = (keyframe["frame"]+1) // 2
            dura  = _time_to_frame(keyframe["time"])

            ## FOR DEBUG
            # if prefix=="Eye" and frame<400: print(keyframe)
            # if "character" in keyframe: print(keyframe["character"])
            ## DEBUG END

            for suffix in ["", "L", "R"]:
                if f"facialPartsDataArray{suffix}" in keyframe:
                    data_array = keyframe[f"facialPartsDataArray{suffix}"]
                    current    = all_current[f"facialPartsDataArray{suffix}"]
                    if suffix: suffix = f"_{suffix}"

                    for part in data_array:
                        id   = part["FacialPartsId"]
                        wp   = part["WeightPer"] * 0.01

                        real_dura = dura if "s_time" not in part else _time_to_frame(part["s_time"])

                        if prefix=="Eye" and keyframe["attribute"]==393216:
                            id = 2
                            weight = 1.0
                            real_dura = 1
                            # blink
                        elif id==0: continue

                        part_key = f"{prefix}_{id}{suffix}"
                        if part_key not in map: map[part_key] = [(part_key, 1.0)]
                        for v in map[part_key]:
                            real_key = v[0]
                            ratio    = v[1]
                            if real_key in current:
                                result.append(MorphFrame(real_key, frame, current[real_key][-1]))
                            else:
                                result.append(MorphFrame(real_key, frame, 0))

                            result.append(MorphFrame(real_key, frame+real_dura, wp*ratio))

                            if prefix=="Eye" and keyframe["attribute"]==393216:
                                result.append(MorphFrame(real_key, frame+real_dura+1, 0))
                            else:
                                current[real_key] = (frame+real_dura, real_dura, wp*ratio)


                    poped = []
                    for k, v in current.items():
                        end_frame = v[0]
                        dura      = v[1]
                        weight    = v[2]
                        if end_frame>frame: continue
                        result.append(MorphFrame(k, frame, weight))
                        result.append(MorphFrame(k, frame+dura, 0))
                        poped.append(k)
                    for k in poped: current.pop(k)


    result.sort(key=lambda x: f"{x.frame:05d}+{x.name}")

    return result

def camera_to_txt():
    pass