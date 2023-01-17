# coding: utf-8
from os import path
from dataclasses import dataclass

from . import UmaMeta, UmaMaster


MASTER_ID = 16
MASTER_CATEGORY = 16


@dataclass
class UmaLive:
    music_id: str
    name:     str
    assets:   list[str]

    def __str__(self) -> str:
        return f"[{self.music_id}] {self.name}"


def _select_assets(master: UmaMaster, keyword: str) -> list[str]:
    return [asset[1] for asset in master.execute(f"SELECT * FROM a WHERE n like ('{keyword}')").fetchall()]


def get_live_list(meta: UmaMeta=None, master: UmaMaster=None, text_data: str="text_data") -> list[UmaLive]:
    default_base = path.join(
        path.expanduser("~"),
        "AppData", "LocalLow", "Cygames", "umamusume"
    )

    if not meta: meta = UmaMeta(default_base)
    if not master: master = UmaMaster(default_base)

    results = []
    live_data_dict = dict()

    for text in master.execute(f"SELECT * FROM {text_data} WHERE id={MASTER_ID} AND category={MASTER_CATEGORY}").fetchall():
        live_data_dict[text[2]] = text

    for live in master.live_data:
        music_id = live["music_id"]

        if music_id in live_data_dict:
            music_name = live_data_dict[music_id][3]

            assets = []
            assets += _select_assets(meta, f"live/musicscores/m{music_id}%") # lyrics / cyalume / ?
            assets += _select_assets(meta, f"sound/l/{music_id}%")
            assets += _select_assets(meta, f"3d/motion/live/body/son{music_id}%")
            assets += _select_assets(meta, f"3d/effect/live/pfb_eff_live_son{music_id}%") # special stage effect
            assets += _select_assets(meta, f"cutt/cutt_son{music_id}%") # ? TimeLine Controller/Camera

            results.append(UmaLive(
                music_id = music_id,
                name = music_name,
                assets = assets,
            ))


    return results



if __name__=="__main__":
    pass