import json
import bpy

from mathutils import Quaternion, Vector

__FPS__ = 30
__MOTION_PATH__ = ""
__BONE_MAP__ = {
    "Position": "Center",
    "Position/Wrist_L_Target": "",
    "Position/Wrist_L_Pole": "",
    "Position/Wrist_R_Target": "",
    "Position/Wrist_R_Pole": "",
    "Position/Foot_L_Target": "",
    "Position/Foot_L_Pole": "ParentNode/LegIKParent_L",
    "Position/Foot_R_Target": "",
    "Position/Foot_R_Pole": "ParentNode/LegIKParent_R",
}

if __name__=="__main__":
    armature_name = ""
    armature = bpy.data.objects[armature_name]

    bpy.context.view_layer.objects.active = armature
    armature.select_set(True)

    bpy.ops.object.mode_set(mode='POSE')

    with open(__MOTION_PATH__, encoding="utf-8") as f:
        data = json.load(f)

    for curve in data["m_RotationCurves"]:
        if curve["path"] not in __BONE_MAP__: continue
        if not __BONE_MAP__[curve["path"]]: continue
        target_bone = __BONE_MAP__[curve["path"]].split("/")[-1]
        bone = armature.pose.bones[target_bone]
        bone.rotation_mode = 'QUATERNION'

        for kf in curve["m_Curve"]:
            bone.rotation_quaternion = Quaternion((kf["value"]["W"], kf["value"]["X"], kf["value"]["Y"], kf["value"]["Z"]))
            bone.keyframe_insert(data_path="rotation_quaternion", frame=int(kf["time"]*__FPS__)+1)

    for curve in data["m_PositionCurves"]:
        if curve["path"] not in __BONE_MAP__: continue
        if not __BONE_MAP__[curve["path"]]: continue
        target_bone = __BONE_MAP__[curve["path"]].split("/")[-1]
        bone = armature.pose.bones[target_bone]

        for kf in curve["m_Curve"]:
            bone.location = Vector((kf["value"]["X"], kf["value"]["Y"], kf["value"]["Z"]))
            bone.keyframe_insert(data_path="location", frame=int(kf["time"]*__FPS__)+1)


    bpy.ops.object.mode_set(mode='OBJECT')