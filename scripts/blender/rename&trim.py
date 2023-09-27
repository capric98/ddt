import bpy

bone_map = {
    "Position": "全ての親",
    "Hip": "下半身",
    "Thigh_L": "左足",
    "Knee_L": "左ひざ",
    "Ankle_L": "左足首",
    "Ankle_offset_L": "",
    "Toe_L": "左つま先",
    "Toe_offset_L": "",
    "Thigh_R": "右足",
    "Knee_R": "右ひざ",
    "Ankle_R": "右足首",
    "Ankle_offset_R": "",
    "Toe_R": "右つま先",
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

if __name__=="__main__":
    for obj in bpy.context.selected_objects:
        if obj.type == "ARMATURE":
            armature = obj
            break

    bpy.context.view_layer.objects.active = armature
    armature.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')

    __TRIM__ = True

    for bone in armature.data.edit_bones:
        if __TRIM__ and bone.name.startswith("Sp_"):
            armature.data.edit_bones.remove(bone)
            continue

        if bone.name not in bone_map or not bone_map[bone.name]: continue
        print(f"{bone.name} -> {bone_map[bone.name]}")
        bone.name = bone_map[bone.name]

    bpy.ops.object.mode_set(mode='OBJECT')