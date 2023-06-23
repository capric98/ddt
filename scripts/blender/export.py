import json
import bpy


bpy.ops.object.select_all(action='DESELECT')
obj = bpy.data.objects["Body"]
target = "C:\\Users\\capric98\\Documents\\MMD\\Motions\\Kirari Magic Show\\1st.json"
fps = 30

if __name__=="__main__":
    
    mdata = {"__config__": {"fps": fps}}
    
    with open(target, "w", encoding="utf-8") as f:
        for fcurve in obj.animation_data.action.fcurves:

            # starts with vector3 & quaternion4 & scale3
            # should be all 0
            if not fcurve.data_path.startswith("pose.bones"): continue
            bone = fcurve.data_path.split("\"")[1]
            kf_type = fcurve.data_path.split("].")[1]

            if bone not in mdata: mdata[bone] = {}
            if kf_type not in mdata[bone]: mdata[bone][kf_type] = {}
            
            for keyframe in fcurve.keyframe_points:
                frame_num = int(keyframe.co[0])
                if frame_num not in mdata[bone][kf_type]: mdata[bone][kf_type][frame_num] = []
                mdata[bone][kf_type][frame_num].append(keyframe.co[1])


        json.dump(mdata, f)