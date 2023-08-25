from dataclasses import dataclass


@dataclass
class MorphFrame:
    name: str
    frame: int
    weight: float

    def __str__(self) -> str:
        return f"{self.name},{self.frame},{self.weight}"


@dataclass
class BoneFrame:
    name: str
    frame: int
    xpos: float
    ypos: float
    zpos: float
    xrot: float
    yrot: float
    zrot: float
    phys_disable: bool = False
    interp_x_ax: float = 20
    interp_x_ay: float = 20
    interp_x_bx: float = 107
    interp_x_by: float = 107
    interp_y_ax: float = 20
    interp_y_ay: float = 20
    interp_y_bx: float = 107
    interp_y_by: float = 107
    interp_z_ax: float = 20
    interp_z_ay: float = 20
    interp_z_bx: float = 107
    interp_z_by: float = 107
    interp_r_ax: float = 20
    interp_r_ay: float = 20
    interp_r_bx: float = 107
    interp_r_by: float = 107

    def __str__(self) -> str:
        return f"{self.name},{self.frame},{self.xpos},{self.ypos},{self.zpos},{self.xrot},{self.yrot},{self.zrot},{self.phys_disable},{self.interp_x_ax},{self.interp_x_ay},{self.interp_x_bx},{self.interp_x_by},{self.interp_y_ax},{self.interp_y_ay},{self.interp_y_bx},{self.interp_y_by},{self.interp_z_ax},{self.interp_z_ay},{self.interp_z_bx},{self.interp_z_by},{self.interp_r_ax},{self.interp_r_ay},{self.interp_r_bx},{self.interp_r_by}"


@dataclass
class CameraFrame:
    frame: int
    dist: float
    target_x: float
    target_y: float
    target_z: float
    x_rot: float
    y_rot: float
    z_rot: float
    fov: float
    perspective: bool = False
    interp_x_ax: float = 20
    interp_x_ay: float = 20
    interp_x_bx: float = 107
    interp_x_by: float = 107
    interp_y_ax: float = 20
    interp_y_ay: float = 20
    interp_y_bx: float = 107
    interp_y_by: float = 107
    interp_z_ax: float = 20
    interp_z_ay: float = 20
    interp_z_bx: float = 107
    interp_z_by: float = 107
    interp_r_ax: float = 20
    interp_r_ay: float = 20
    interp_r_bx: float = 107
    interp_r_by: float = 107
    interp_dist_ax: float = 20
    interp_dist_bx: float = 107
    interp_dist_ay: float = 20
    interp_dist_by: float = 107
    interp_fov_ax: float = 20
    interp_fov_bx: float = 107
    interp_fov_ay: float = 20
    interp_fov_by: float = 107

    def __str__(self) -> str:
        return f"{self.frame},{self.dist},{self.target_x},{self.target_y},{self.target_z},{self.x_rot},{self.y_rot},{self.z_rot},{self.fov},{self.perspective},{self.interp_x_ax},{self.interp_x_ay},{self.interp_x_bx},{self.interp_x_by},{self.interp_y_ax},{self.interp_y_ay},{self.interp_y_bx},{self.interp_y_by},{self.interp_z_ax},{self.interp_z_ay},{self.interp_z_bx},{self.interp_z_by},{self.interp_r_ax},{self.interp_r_ay},{self.interp_r_bx},{self.interp_r_by},{self.interp_dist_ax},{self.interp_dist_bx},{self.interp_dist_ay},{self.interp_dist_by},{self.interp_fov_ax},{self.interp_fov_bx},{self.interp_fov_ay},{self.interp_fov_by}"


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

def _time_to_frame(time, fps=30):
    return round(time*fps*0.02)

def parse_facial(camera_fn, chara_id, map={}, fps=30) -> list[MorphFrame]:
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
    if "ripSync2Keys" in tree and "thisList" in tree["ripSync2Keys"]:
        for v in tree["ripSync2Keys"]["thisList"]:
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
            frame = int(0.01 + keyframe["frame"] / (60/fps))
            dura  = _time_to_frame(keyframe["time"], fps)

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
                            real_dura = int(0.01 + 4*fps/60)
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
                                result.append(MorphFrame(real_key, frame+real_dura+int(0.01 + 4*fps/60), 0))
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

def parse_eyetrack(camera_fn, chara_id, bone_name: list[str]={"左目", "右目"}, scale: float=0.6) -> list[BoneFrame]:
    import UnityPy
    from math import asin, degrees
    for obj in UnityPy.load(camera_fn).objects:
        if obj.type.name == "MonoBehaviour":
            if obj.serialized_type.nodes:
                tree = obj.read_typetree()

    data = tree["facial1Set"] if chara_id==1 else tree["other4FacialArray"][chara_id-2]
    data = data["eyeTrackKeys"]["thisList"]

    last   = None
    result = []

    for keyframe in data:
        frame = (keyframe["frame"]+1) // 2
        dura  = _time_to_frame(keyframe["time"])

        direct_pos = keyframe["DirectPosition"]
        dx, dy, dz = direct_pos["x"], direct_pos["y"], direct_pos["z"]

        if abs(dx)<1e-6 and abs(dy)<1e-6 and abs(dx)<1e-6:
            dx = dy = 0
            dz = 1

        norm = (dx**2 + dy**2 + dz**2) ** 0.5
        dx   = dx / norm
        dy   = dy / norm
        dz   = dz / norm

        xrot = degrees(asin(dy)) * scale
        yrot = degrees(asin(dx)) * scale
        zrot = 0 * scale

        if not last: last = (0,0,0)
        for bone in bone_name:
            result.append(BoneFrame(bone,frame,0,0,0,last[0],last[1],last[2]))
            result.append(BoneFrame(bone,frame+dura,0,0,0,xrot,-yrot,zrot))

        last = (xrot,-yrot,zrot)

    return result

# not finished...
def parse_camera(camera_fn) -> None:
    import UnityPy
    from math import degrees
    for obj in UnityPy.load(camera_fn).objects:
        if obj.type.name == "MonoBehaviour":
            if obj.serialized_type.nodes:
                tree = obj.read_typetree()

    kf_dict = {}
    kf_list = []

    for keyframe in tree["cameraPosKeys"]["thisList"]:
        frame = (keyframe["frame"]+1) // 2
        if frame not in kf_list:
            kf_list.append(frame)
            kf_dict[frame] = []
        kf_dict[frame].append((-keyframe["position"]["x"],keyframe["position"]["y"],keyframe["position"]["z"]))
    for keyframe in tree["cameraLookAtKeys"]["thisList"]:
        frame = (keyframe["frame"]+1) // 2
        if frame not in kf_list:
            kf_list.append(frame)
            kf_dict[frame] = []
        kf_dict[frame].append((-keyframe["position"]["x"],keyframe["position"]["y"],keyframe["position"]["z"]))
    for keyframe in tree["cameraFovKeys"]["thisList"]:
        frame = (keyframe["frame"]+1) // 2
        if frame not in kf_list:
            kf_list.append(frame)
            kf_dict[frame] = []
        if keyframe["fovType"]==0:
            kf_dict[frame].append(keyframe["fov"])
        else:
            kf_dict[frame].append(degrees(keyframe["fov"])) # my guess

    kf_list.sort()
    keyframes = [([v]+kf_dict[v]) for v in kf_list]
    result = []

    for kf in keyframes:
        if len(kf)!=4:continue
        dx, dy, dz = kf[1][0]-kf[2][0], kf[1][1]-kf[2][1], kf[1][2]-kf[2][2]
        dist = (dx**2+dy**2+dz**2) ** 0.5
        # result.append(CameraFrame(kf[0],dist,kf[2][0],kf[2][1],kf[2][2],0,0,0,kf[3]))


def camera_to_txt():
    pass