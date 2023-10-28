import bpy
from math import radians
from mathutils import Quaternion


frame_range = (8688//2, (8688+2480)//2)

main_armature = None
new_armature  = None

diff = (0, 0, 0)


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


def init():
    global main_armature, new_armature

    for obj in bpy.data.objects:
        if obj.type == "ARMATURE":
            if obj.name.startswith("pfb_bdy") and obj.name.endswith(".001") and new_armature is None:
                new_armature = obj
            else:
                main_armature = obj


if __name__=="__main__":
    init()


    for k in range(frame_range[0], frame_range[1]):
        print(k)

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.scene.frame_set(k)

        bpy.context.view_layer.objects.active = new_armature
        new_armature.select_set(True)
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action='SELECT')
        bpy.ops.pose.copy()
        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.context.view_layer.objects.active = main_armature
        main_armature.select_set(True)
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action='SELECT')
        bpy.ops.pose.paste()
        bpy.ops.anim.keyframe_insert()
