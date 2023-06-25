from dataclasses import dataclass

@dataclass
class Position:
    x: float
    y: float
    z: float

@dataclass
class FacialPartsData:
    part: str
    id: int
    weight: float
    s_time: float

@dataclass
class ThisListComponent:
    frame: int
    time: float
    # attribute: int
    facialPartsDataArray: list[FacialPartsData]
    directPosition: Position

@dataclass
class MorphFrame:
    name: str
    frame: int
    weight: float


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

def _parse_facial_part(prefix, target, data):
    data = data[f"{prefix}Keys"]["thisList"]
    result = []

    for v in data:

        frame = (v["frame"]+1)//2 # 60->30
        dura  = _time_to_frame(v["time"])

        for suffix in ["", "L", "R"]:
            if f"facialPartsDataArray{suffix}" in v:
                parts = v[f"facialPartsDataArray{suffix}"]
                if suffix: suffix=f"_{suffix}"

                for part in parts:

                    id = part["FacialPartsId"]
                    weight = part["WeightPer"] * 0.01
                    real_dura = dura if "s_time" not in part else _time_to_frame(part["s_time"])

                    if prefix=="eye" and v["attribute"]==393216:
                        id = 2
                        weight = 1.0
                        real_dura = 1
                        # blink
                    elif id==0: continue

                    if frame>0:
                        result.append(MorphFrame(
                            name=f"{target}_{id}{suffix}",
                            frame=frame-1,
                            weight=0,
                        ))
                    result.append(MorphFrame(
                        name=f"{target}_{id}{suffix}",
                        frame=frame,
                        weight=weight,
                    ))
                    result.append(MorphFrame(
                        name=f"{target}_{id}{suffix}",
                        frame=frame+real_dura,
                        weight=0,
                    ))

    result.sort(key=lambda x: f"{x.name}+{x.frame:05d}")

    return result

def parse_facial(camera_fn, chara_id) -> list[MorphFrame]:
    import UnityPy

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
        data["mouthKeys"]["thisList"].extend(tree["ripSyncKeys"]["thisList"])

    result = []
    result.extend(_parse_facial_part("mouth", "Mouth", data))
    result.extend(_parse_facial_part("eye", "Eye", data))
    result.extend(_parse_facial_part("eyebrow", "Ebrow", data))
    # eyetrack pass

    result.sort(key=lambda x: f"{x.name}+{x.frame:05d}")

    for k in range(len(result)-1):
        if result[k].name!=result[k+1].name and result[k].weight<1e-3:
            result[k].name = "__TRAILING__"

    return result


def camera_to_txt():
    pass