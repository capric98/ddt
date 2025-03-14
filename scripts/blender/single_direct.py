#!/usr/bin/env python3
# coding: utf-8

from pathlib import Path
home_dir = Path.home()

import math
import UnityPy

try:
    from mathutils import Quaternion
    import bpy
except ImportError:
    __IS_IN_BLENDER__ = False
else:
    __IS_IN_BLENDER__ = True


def get_leaf_bone(bone: str) -> str:
    return bone.split("/")[-1]

def find_armature(obj):
    if obj.type == "ARMATURE": return obj
    for child in obj.children:
        if child.type == "ARMATURE":
            return child
        elif child.type == "MESH":
            armature = child.find_armature()
            if armature: return armature

def create_fcurves(action, bone_name: str, data_path: str, num_dimensions: int):
    """创建指定维度的F曲线"""
    for i in range(num_dimensions):
        action.fcurves.new(
            data_path=f"pose.bones[\"{bone_name}\"].{data_path}",
            index=i,
            action_group=bone_name
        )

def insert_keyframe(action, data_path, frame, values, interp_func: str="LINEAR"):
    for i, value in enumerate(values):
        fc = action.fcurves.find(data_path, index=i)
        if fc:
            fc.keyframe_points.add(1)
            kp = fc.keyframe_points[-1]
            kp.co = (frame, value)
            kp.interpolation = interp_func

def quatf_to_tuple(quat, profile=["w", "x", "y", "z"]):
    qlist = [0] * len(profile)
    for k in range(len(profile)):
        w = -1 if profile[k].startswith("-") else 1
        v = getattr(quat, profile[k][-1])
        qlist[k] = w * v

    return tuple(qlist)

def apply_anim(fn: str, mmd_obj, bone_map: dict, fps: int=30):

    anim = UnityPy.load(fn)
    clip = None

    for k, v in anim.container.items():
        if v.type.name == "AnimationClip":
            clip_name = k
            clip = v.read()
            break

    if not clip: raise ValueError(f"AnimationClip not found in {fn}")

    if __IS_IN_BLENDER__:
        mmd_armature = find_armature(mmd_obj)
        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.view_layer.objects.active = mmd_armature
        mmd_armature.select_set(True)

        anim_action = bpy.data.actions.new(name=get_leaf_bone(clip_name))
        mmd_armature.animation_data_create()
        mmd_armature.animation_data.action = anim_action

    for curve in clip.m_PositionCurves:
        uma_bone = get_leaf_bone(curve.path)
        mmd_bone = bone_map.get(uma_bone, "")
        if not mmd_bone: continue

        # curve.curve.(m_Curve, m_PostInfinity, m_PreInfinity, m_RotationOrder=4)
        print(f"{uma_bone} has {len(curve.curve.m_Curve)} keyframes in m_PositionCurves")
        if __IS_IN_BLENDER__: create_fcurves(anim_action, mmd_bone, "location", 3)

        for keyframe in curve.curve.m_Curve:
            if __IS_IN_BLENDER__:
                insert_keyframe(
                    anim_action,
                    f"pose.bones[\"{mmd_bone}\"].location",
                    int(keyframe.time * fps),
                    (keyframe.value.x, keyframe.value.y, keyframe.value.z),
                )

    profile_dict = {
        "__DEFAULT__": ["w", "x", "y", "z"],
        "Hip": ["-w", "-x", "y", "z"],
        "Thigh_L": ["x", "-w", "-z", "y"],
        "Thigh_R": ["x", "-w", "-z", "y"],
        "Knee_L": ["w", "x", "y", "z"],
        "Knee_R": ["w", "x", "y", "z"],
        # Ankle_L
        # Toe_L
        # Thigh_R
        # Ankle_R
        # Toe_R
        # Waist
        # Spine
        # Chest
        # Neck
        # Head
        # Shoulder_L
        # Arm_L
        # Elbow_L
        # ArmRoll_L
        # Wrist_L
        # Thumb_01_L
        # Thumb_02_L
        # Thumb_03_L
        # Index_01_L
        # Index_02_L
        # Index_03_L
        # Middle_01_L
        # Middle_02_L
        # Middle_03_L
        # Ring_01_L
        # Ring_02_L
        # Ring_03_L
        # Pinky_01_L
        # Pinky_02_L
        # Pinky_03_L
        # Shoulder_R
        # Arm_R
        # Elbow_R
        # ArmRoll_R
        # Wrist_R
        # Thumb_01_R
        # Thumb_02_R
        # Thumb_03_R
        # Pinky_01_R
        # Pinky_02_R
        # Pinky_03_R
        # Ring_01_R
        # Ring_02_R
        # Ring_03_R
        # Middle_01_R
        # Middle_02_R
        # Middle_03_R
        # Index_01_R
        # Index_02_R
        # Index_03_R
    }

    for curve in clip.m_RotationCurves:
        uma_bone = get_leaf_bone(curve.path)
        mmd_bone = bone_map.get(uma_bone, "")
        if not mmd_bone:
            print(curve.path)
            continue

        print(f"{uma_bone} has {len(curve.curve.m_Curve)} keyframes in m_RotationCurves")
        if __IS_IN_BLENDER__:
            if curve.curve.m_RotationOrder!=4: raise ValueError(f"m_RotationOrder == {curve.curve.m_RotationOrder}")
            create_fcurves(anim_action, mmd_bone, "rotation_quaternion", curve.curve.m_RotationOrder)

        for keyframe in curve.curve.m_Curve:
            if __IS_IN_BLENDER__:
                pname = uma_bone if uma_bone in profile_dict else "__DEFAULT__"
                if pname != "__DEFAULT__":
                    insert_keyframe(
                        anim_action,
                        f"pose.bones[\"{mmd_bone}\"].rotation_quaternion",
                        int(keyframe.time * fps),
                        quatf_to_tuple(keyframe.value, profile_dict[pname]),
                    )


if __name__ == "__main__":

    mmd_obj = None if not __IS_IN_BLENDER__ else bpy.context.object
    anim_fn = str(home_dir.joinpath("Documents\\MMD\Motion\\[1151] Legend-Changer\\extract\\motion\\anm_liv_son1151_1st"))

    bone_map={
        "Position": "全ての親",
        "Hip": "センター",
        "Thigh_L": "左足",
        "Knee_L": "左ひざ",
        "Ankle_L": "左足首",
        "Ankle_offset_L": "",
        "Toe_L": "左足先EX",
        "Toe_offset_L": "",
        "Thigh_R": "右足",
        "Knee_R": "右ひざ",
        "Ankle_R": "右足首",
        "Ankle_offset_R": "",
        "Toe_R": "右足先EX",
        "Toe_offset_R": "",
        "UpBody_Ctrl": "",
        "Waist": "上半身",
        "Spine": "上半身3",
        "Chest": "上半身2",
        "Neck": "首",
        "Head": "頭",
        "Shoulder_L": "左肩",
        "ShoulderRoll_L": "",
        "Arm_L": "左腕",
        "Elbow_L": "左ひじ",
        "ArmRoll_L": "左手捩",
        "Wrist_L": "左手首",
        "Hand_Attach_L": "",
        "Thumb_01_L": "左親指０",
        "Thumb_02_L": "左親指１",
        "Thumb_03_L": "左親指２",
        "Index_01_L": "左人指１",
        "Index_02_L": "左人指２",
        "Index_03_L": "左人指３",
        "Middle_01_L": "左中指１",
        "Middle_02_L": "左中指２",
        "Middle_03_L": "左中指３",
        "Ring_01_L": "左薬指１",
        "Ring_02_L": "左薬指２",
        "Ring_03_L": "左薬指３",
        "Pinky_01_L": "左小指１",
        "Pinky_02_L": "左小指２",
        "Pinky_03_L": "左小指３",
        "Shoulder_R": "右肩",
        "ShoulderRoll_R": "",
        "Arm_R": "右腕",
        "Elbow_R": "右ひじ",
        "ArmRoll_R": "右手捩",
        "Wrist_R": "右手首",
        "Hand_Attach_R": "",
        "Thumb_01_R": "右親指０",
        "Thumb_02_R": "右親指１",
        "Thumb_03_R": "右親指２",
        "Index_01_R": "右人指１",
        "Index_02_R": "右人指２",
        "Index_03_R": "右人指３",
        "Middle_01_R": "右中指１",
        "Middle_02_R": "右中指２",
        "Middle_03_R": "右中指３",
        "Ring_01_R": "右薬指１",
        "Ring_02_R": "右薬指２",
        "Ring_03_R": "右薬指３",
        "Pinky_01_R": "右小指１",
        "Pinky_02_R": "右小指２",
        "Pinky_03_R": "右小指３",
    }

    if __IS_IN_BLENDER__:
        bpy.ops.mmd_tools.import_model(filepath=str(home_dir.joinpath("Documents\\MMD\\Model\\Helios.renamed.pmx")), scale=0.08, rename_bones=False)
        mmd_obj = bpy.context.active_object

    apply_anim(anim_fn, mmd_obj, bone_map)