import bpy
from math import radians
from mathutils import Quaternion


target_frame = 5000
uma_armature = bpy.data.objects["pfb_bdy10xx_xx"] # ARMATURE NAME HERE
new_armature = bpy.data.objects["xxx_arm"]        # ARMATURE NAME HERE


def copy_pose(bone_name, pre_rot=0):
    # print(bone_name)
    bpy.ops.object.mode_set(mode='POSE')
    a_bone = uma_armature.pose.bones.get(bone_name)
    t_bone = new_armature.pose.bones.get(bone_name)
    if a_bone is None or t_bone is None:
        print("One or both of the specified bones do not exist.")
        return

    aq = a_bone.matrix.to_quaternion()
    tq = Quaternion(t_bone.vector, radians(pre_rot)) @ t_bone.matrix.to_quaternion()

    rotation =  aq.rotation_difference(tq)

    a_bone.rotation_mode = 'QUATERNION'
    a_bone.rotation_quaternion = rotation
    a_bone.keyframe_insert("rotation_quaternion", frame=target_frame)
    bpy.ops.object.mode_set(mode='OBJECT')


if __name__=="__main__":
    print("==IDK why but it works...==")
    bpy.context.scene.frame_set(target_frame)
    bpy.context.view_layer.objects.active = uma_armature
    uma_armature.select_set(True)
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.transforms_clear()

    # The following angles need to be carefully tweaked on specific model.
    copy_pose("左腕", 135)
    copy_pose("左ひじ", 135)
    copy_pose("右腕", -135)
    copy_pose("右ひじ", -135)

    copy_pose("左親指０", 135)
    copy_pose("左親指１", 135)
    copy_pose("右親指０", 45)
    copy_pose("右親指１", 45)

    for n in ["人指１", "人指２", "人指３", "中指１", "中指２", "中指３", "薬指１", "薬指２", "薬指３", "小指１", "小指２", "小指３"]:
        if "３" in n: continue
        copy_pose("左"+n, 35)
        copy_pose("右"+n, 125)
