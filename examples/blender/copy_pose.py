import bpy
from mathutils import Quaternion, Vector


target_frame = 1800
uma_armature = bpy.data.objects[""] # ARMATURE NAME HERE
new_armature = bpy.data.objects[""] # ARMATURE NAME HERE


def copy_pose_L(bone_name):
    # print(bone_name)
    bpy.ops.object.mode_set(mode='POSE')
    a_bone = uma_armature.pose.bones.get(bone_name)
    t_bone = new_armature.pose.bones.get(bone_name)
    if a_bone is None or t_bone is None:
        print("One or both of the specified bones do not exist.")
        return

    a_vec = a_bone.tail - a_bone.head
    t_vec = t_bone.tail - t_bone.head

    n_vec = a_vec.cross(t_vec)
    n_vec.normalize()

    theta = a_vec.angle(t_vec)
    # ctheta = acos(a_vec@t_vec / (a_vec.length*t_vec.length))
    # print(a_vec)
    # print(t_vec)
    # print(n_vec, theta/3.14159*180, ctheta/3.14159*180)

    rotation = Quaternion(Vector((n_vec[2], n_vec[0], n_vec[1])), theta)
    #rotation = a_vec.rotation_difference(t_vec)
    #rotation = Quaternion((rotation[0], rotation[1], rotation[3], rotation[2]))
    if "中指" in bone_name: rotation = Quaternion(Vector((-n_vec[0], -n_vec[1], -n_vec[2])), theta)
    if "薬指" in bone_name: rotation = Quaternion(Vector((n_vec[0], -n_vec[1], -n_vec[2])), theta)
    if "小指" in bone_name: rotation = Quaternion(Vector((n_vec[0], -n_vec[1], -n_vec[2])), theta)

    a_bone.rotation_mode = 'QUATERNION'
    a_bone.rotation_quaternion = rotation
    a_bone.keyframe_insert("rotation_quaternion", frame=target_frame)
    bpy.ops.object.mode_set(mode='OBJECT')


def copy_pose_R(bone_name):
    # print(bone_name)
    bpy.ops.object.mode_set(mode='POSE')
    a_bone = uma_armature.pose.bones.get(bone_name)
    t_bone = new_armature.pose.bones.get(bone_name)
    if a_bone is None or t_bone is None:
        print("One or both of the specified bones do not exist.")
        return

    a_vec = a_bone.tail - a_bone.head
    t_vec = t_bone.tail - t_bone.head

    n_vec = a_vec.cross(t_vec)
    n_vec.normalize()

    theta = a_vec.angle(t_vec)
    # print(a_vec)
    # print(t_vec)
    # print(n_vec, theta/3.1415926*180)

    rotation = Quaternion(Vector((n_vec[2], n_vec[0], -n_vec[1])), theta)
    if "指" in bone_name: rotation = Quaternion(Vector((-n_vec[2], -n_vec[0], n_vec[1])), theta)
    if "中指" in bone_name: rotation = Quaternion(Vector((-n_vec[0], -n_vec[1], -n_vec[2])), theta)
    if "薬指" in bone_name: rotation = Quaternion(Vector((n_vec[0], -n_vec[1], -n_vec[2])), theta)
    if "小指" in bone_name: rotation = Quaternion(Vector((n_vec[0], -n_vec[1], -n_vec[2])), theta)

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

    for n in ["腕", "ひじ", "手首", "親指０", "親指１", "親指２", "人指１", "人指２", "中指１", "中指２", "薬指１", "薬指２", "小指１", "小指２"]:
        copy_pose_L("左"+n)
    for n in ["腕", "ひじ", "手首", "親指０", "親指１", "親指２", "人指１", "人指２", "人指３", "中指１", "中指２", "中指３", "薬指１", "薬指２", "薬指３", "小指１", "小指２", "小指３"]:
        copy_pose_R("右"+n)