# coding: utf-8
import argparse
from pathlib import Path

import UnityPy


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="umamusume camera edit",
        description="nothing",
        epilog="_(:з」∠)_",
    )

    parser.add_argument("fn", type=str)
    args = parser.parse_args()
    fn = Path(args.fn)

    camera = UnityPy.load(str(fn))
    for obj in camera.objects:
        if obj.type.name == "MonoBehaviour":
            mb = obj.read_typetree()

    # for k in mb:
    #     print(k)
        # objectList too many
        # propsList
        # propsAttachList

    motion_list = mb["charaMotSeqList"]
    print(f"find {len(motion_list)} records in charaMotSeqList")
    with open(fn.parent.absolute().joinpath(fn.name+".charaMotSeqList.txt"), "w", encoding="utf-8") as f:
        for num in range(len(motion_list)):
            print(f"character number {num}:", file=f)

            shortest_mn = " " * 1000

            for motion in motion_list[num]["keys"]["thisList"]:
                frame  = motion["frame"]
                mname  = motion["motionName"]
                hframe = motion["motionHeadFrame"]
                length = motion["playFrameLength"]

                print(f"  frame = {int(frame/2)} (t={frame/60:.2f}s), play \"{mname}\" from {int(hframe/2)} to {int((hframe+length)/2)}", file=f)

                ffinal = frame + length
                shortest_mn = shortest_mn if len(shortest_mn) < len(mname) else mname

            print(f"  final frame = {ffinal}", file=f)
            print("", file=f)

            print(f"change #{num} motion to play full of {shortest_mn} from 0 to {ffinal}")
            motion_list[num]["keys"]["thisList"] = motion_list[num]["keys"]["thisList"][:1]
            motion_list[num]["keys"]["thisList"][0]["frame"] = 0
            motion_list[num]["keys"]["thisList"][0]["motionName"] = shortest_mn
            motion_list[num]["keys"]["thisList"][0]["motionHeadFrame"] = 0
            motion_list[num]["keys"]["thisList"][0]["playFrameLength"] = ffinal
            # print(len(motion_list[num]["keys"]["thisList"]))


    mb["charaMotSeqList"] = motion_list
    mb["tiltShiftKeys"]["thisList"] = mb["tiltShiftKeys"]["thisList"][:1]

    # for tf_k in range(len(mb["transformList"])):
    #     for k in range(len(mb["transformList"][tf_k]["keys"]["thisList"])):
    #         mb["transformList"][tf_k]["keys"]["thisList"][k]["position"] = {"x": 0.0, "y": 0.0, "z": 0.0}

    # for cm_key in ["cameraPosKeys", "cameraLookAtKeys", "cameraFovKeys", "cameraRollKeys", "cameraMotionKeys"]:
    #     for k in range(len(mb[cm_key]["thisList"])):
    #         for pos_key in ["charaPos", "position", "CharaPositionAtStartFrame"]:
    #             if pos_key in mb[cm_key]["thisList"][k]:
    #                 mb[cm_key]["thisList"][k][pos_key] = {"x": 0.0, "y": 0.0, "z": 0.0}

    form_offset = mb["formationOffsetSet"]
    for form_key in form_offset:
        for k in range(len(form_offset[form_key]["thisList"])):
            form_offset[form_key]["thisList"][k]["visible"] = 1
            form_offset[form_key]["thisList"][k]["isEnabledOffset"] = 0
            form_offset[form_key]["thisList"][k]["IsPositionAddParentNode"] = 0
            form_offset[form_key]["thisList"][k]["posXZ"] = {"x": 0.0, "y": 0.0}
            form_offset[form_key]["thisList"][k]["posY"] = 0.0
            form_offset[form_key]["thisList"][k]["RotationY"] = 0.0
            form_offset[form_key]["thisList"][k]["LocalRotationY"] = 0.0
            for pos_key in ["Position", "position", "offsetMaxPosition", "offsetMinPosition", "WorldSpaceOrigin"]:
                form_offset[form_key]["thisList"][k][pos_key] = {"x": 0.0, "y": 0.0, "z": 0.0}
    mb["formationOffsetSet"] = form_offset

    obj.save_typetree(mb)

    fn.parent.absolute().joinpath("modified_1motion").mkdir(exist_ok=True)
    camera.save(pack="lz4", out_path=str(fn.parent.absolute().joinpath("modified_1motion")))
