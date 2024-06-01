# coding: utf-8
from os import path
from dataclasses import dataclass
from sqlite3 import Connection

from . import UmaBlob, UmaMeta, UmaMaster


MASTER_ID = 16
MASTER_CATEGORY = 16


@dataclass
class UmaLive:
    music_id: str
    name:     str
    # assets:   list[UmaBlob]
    meta:     Connection
    def __str__(self) -> str:
        return f"[{self.music_id}] {self.name}"

    @property
    def assets(self) -> list[UmaBlob]:
        assets = []
        assets += _select_assets(self.meta, f"live/musicscores/m{self.music_id}%") # lyrics / cyalume / ?
        assets += _select_assets(self.meta, f"sound/l/{self.music_id}%")
        # assets += _select_assets(self.meta, f"sound/b/snd_bgm_cs{self.music_id}%") # just in case
        assets += _select_assets(self.meta, f"3d/motion/live/body/son{self.music_id}%")
        assets += _select_assets(self.meta, f"3d/effect/live/pfb_eff_live_son{self.music_id}%") # special stage effect
        assets += _select_assets(self.meta, f"cutt/cutt_son{self.music_id}%") # ? TimeLine Controller/Camera

        assets += _select_assets(self.meta, f"livesettings")

        # livesettings
        # id,type,param1,param2,param3,param4,param5
        # 1,0,Cutt_son1059,,,,
        # 2,1,10124,0,,,
        # 3d/env/live/live10124/pfb_env_live10124_controller000

        return assets


def _select_assets(master: UmaMaster, keyword: str) -> list[UmaBlob]:
    return [UmaBlob(
        type = item[7],
        id = item[0],
        hash = item[6],
        path = item[1],
    ) for item in master.execute(f"SELECT * FROM a WHERE n like ('{keyword}')").fetchall()]

def select_dependencies(master: UmaMaster, keyword: str) -> list[UmaBlob]:
    record = master.execute(f"SELECT * FROM a WHERE n like ('{keyword}')").fetchone()
    dependencies = []

    dependencies.append(UmaBlob(
        type = record[7],
        id = record[0],
        hash = record[6],
        path = record[1],
    ))

    for d in record[2].split(";"):
        if d=="shader": continue
        item = master.execute(f"SELECT * FROM a WHERE n like ('{d}')").fetchone()

        dependencies.append(UmaBlob(
            type = item[7],
            id = item[0],
            hash = item[6],
            path = item[1],
        ))

    return dependencies


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

            results.append(UmaLive(
                music_id = music_id,
                name = music_name,
                meta = meta,
            ))


    return results



if __name__=="__main__":
    pass