import bpy
import os

from math import radians, degrees
from mathutils import Quaternion


def delete_hierarchy(obj):
    for child in obj.children:
        delete_hierarchy(child)

    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.ops.object.delete()


def import_fbx(fn: str) -> tuple[bpy.types.Object, int]:
    bpy.ops.better_import.fbx(filepath=fn, my_fbx_unit="m")

    obj = bpy.context.active_object
    anim_len = 0

    for fcurve in obj.animation_data.action.fcurves:
        if len(fcurve.keyframe_points) > anim_len:
            anim_len = len(fcurve.keyframe_points)

    # bpy.context.scene.frame_set(target_frame)

    return (obj, anim_len)


def import_mmd(fn: str) -> bpy.types.Object:
    bpy.ops.mmd_tools.import_model(filepath=fn, scale=0.08, rename_bones=False)
    return bpy.context.active_object


def export_vmd(obj: bpy.types.Object, fn: str):
    try:
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
    except:
        pass

    bpy.ops.mmd_tools.export_vmd(filepath=fn, use_pose_mode=True, use_frame_range=True)



def uma_bones_to_mmd(obj: bpy.types.Object, bone_map: dict, trim: bool=False):

    armature = None

    bpy.ops.object.select_all(action="DESELECT")
    for child in obj.children:
        if child.type == "MESH":
            child.select_set(trim)
            armature = child.find_armature() if not armature else armature

    if trim: bpy.ops.object.delete()
    bpy.ops.object.select_all(action="DESELECT")

    bpy.context.view_layer.objects.active = armature
    armature.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")

    for bone in armature.data.edit_bones:
        if trim and bone.name.startswith("Sp_"):
            print(f"deleted {bone.name}")
            armature.data.edit_bones.remove(bone)
            continue

        if bone.name not in bone_map or not bone_map[bone.name]: continue
        print(f"renamed {bone.name} -> {bone_map[bone.name]}")
        bone.name = bone_map[bone.name]

    bpy.ops.object.mode_set(mode='OBJECT')


def find_armature(obj: bpy.types.Object) -> bpy.types.Object:
    if obj.type == "ARMATURE": return obj
    for child in obj.children:
        if child.type == "ARMATURE":
            return child
        elif child.type == "MESH":
            armature = child.find_armature()
            if armature: return armature


def copy_pose(uma_obj: bpy.types.Object, mmd_obj: bpy.types.Object, frame_num: int, preset: dict):

    bpy.context.scene.frame_set(frame_num)

    uma_armature = find_armature(uma_obj)
    mmd_armature = find_armature(mmd_obj)

    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = uma_armature
    uma_armature.select_set(True)

    # clear pose
    bpy.ops.object.mode_set(mode="POSE")
    bpy.ops.pose.select_all(action="SELECT")
    bpy.ops.pose.transforms_clear()

    def _debug_euler(e):
        return f"x={degrees(e[0]):.2f}, y={degrees(e[1]):.2f}, z={degrees(e[2]):.2f}"

    def _copy_pose(uma_armature, mmd_armature, bone_name, rot):
        # TODO: fix finger
        # if "指" in bone_name: return
        bpy.ops.object.mode_set(mode="POSE")

        uma_bone = uma_armature.pose.bones.get(bone_name)
        mmd_bone = mmd_armature.pose.bones.get(bone_name)

        if uma_bone is None or mmd_bone is None:
            print("One or both of the specified bones do not exist.")
            return

        uma_quaternion = uma_bone.matrix.to_quaternion()
        mmd_quaternion = mmd_bone.matrix.to_quaternion()
        mmd_quaternion.rotate(Quaternion(mmd_bone.vector, radians(rot)))

        rotation = uma_quaternion.rotation_difference(mmd_quaternion)

        uma_bone.rotation_mode = "QUATERNION"
        uma_bone.rotation_quaternion = rotation
        uma_bone.keyframe_insert("rotation_quaternion", frame=frame_num)

        bpy.ops.object.mode_set(mode="OBJECT")


    for bone_name, rot in preset.items():
        if isinstance(rot, list):
            for finger_name in ["人指１", "人指２", "人指３", "中指１", "中指２", "中指３", "薬指１", "薬指２", "薬指３", "小指１", "小指２", "小指３"]:
                if "３" in finger_name: continue
                _copy_pose(uma_armature, mmd_armature, "左"+finger_name, rot[0])
                _copy_pose(uma_armature, mmd_armature, "右"+finger_name, rot[1])
        else:
            _copy_pose(uma_armature, mmd_armature, bone_name, rot)

    bpy.ops.object.mode_set(mode="OBJECT")


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


# The following angles need to be carefully tweaked on specific model.
presets = {
    "_DEFAULTS_": {
        "左腕": 90,
        "左ひじ": 90,
        "右腕": -90,
        "右ひじ": -90,
        "左親指０": -180,
        "左親指１": -180,
        "右親指０": 0,
        "右親指１": 0,
        "_FINGERS_": [180, 0],
    }
}
presets.update(dict.fromkeys(["青雀"], {
    "左腕": 135,
    "左ひじ": 135,
    "右腕": -135,
    "右ひじ": -135,
    "左親指０": 135,
    "左親指１": 135,
    "右親指０": 45,
    "右親指１": 45,
    "_FINGERS_": [35, 125],
}))
presets.update(dict.fromkeys(["符玄", "克拉拉", "桂乃芬", "原神"], {
    "左腕": -90,
    "左ひじ": -90,
    "右腕": 90,
    "右ひじ": 90,
    "左親指０": -90,
    "左親指１": -90,
    "右親指０": -90,
    "右親指１": -90,
    "_FINGERS_": [180, 0],
}))
presets.update(dict.fromkeys(["琳妮特"], {
    "左腕": -90,
    "左ひじ": -90,
    "右腕": 90,
    "右ひじ": 90,
    "左親指０": -90,
    "左親指１": -90,
    "右親指０": -90,
    "右親指１": -90,
    "_FINGERS_": [0, 180],
}))
presets.update(dict.fromkeys(["绮良良"], {
    "左腕": -90,
    "左ひじ": -90,
    "右腕": 90,
    "右ひじ": 90,
    "左親指０": 90,
    "左親指１": 90,
    "右親指０": 90,
    "右親指１": 90,
    "_FINGERS_": [0, 180],
}))
presets.update(dict.fromkeys(["花火"], {
    "左腕": -90,
    "左ひじ": -90,
    "右腕": 90,
    "右ひじ": 90,
    "左親指０": -90,
    "左親指１": -90,
    "右親指０": -90,
    "右親指１": -90,
    "_FINGERS_": [180, 0],
}))
presets.update(dict.fromkeys(["知更鸟"], {
    "左腕": 90,
    "左ひじ": 90,
    "右腕": -90,
    "右ひじ": -90,
    "左親指０": 90,
    "左親指１": 90,
    "右親指０": 90,
    "右親指１": 90,
    "_FINGERS_": [0, 180],
}))


if __name__ == "__main__":

    __DEBUG_PRESET__ = True

    pmx_path = ""
    fbx_dir = ""
    output_dir = ""

    pmx_name = "_DEFAULTS_" # This is used to find the preset to copy the pose.


    mmd_obj = import_mmd(pmx_path)

    for f in os.listdir(fbx_dir):
        if f.lower().endswith(".fbx"):
            fn = os.path.join(fbx_dir, f)

            # import fbx file
            uma_obj, anim_len = import_fbx(fn)
            bpy.data.scenes["Scene"].frame_end = anim_len

            # rename bones
            uma_bones_to_mmd(uma_obj, bone_map, trim=not __DEBUG_PRESET__)

            # copy pose
            copy_pose(uma_obj, mmd_obj, anim_len+100, preset=presets[pmx_name])

            if __DEBUG_PRESET__: break

            output_fn = os.path.splitext(os.path.basename(f))[0]
            output_fn = os.path.join(output_dir, output_fn+".vmd")
            export_vmd(uma_obj, output_fn)

            # delete the fbx animation
            delete_hierarchy(uma_obj)