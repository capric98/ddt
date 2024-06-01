#!/usr/bin/env python3
# coding: utf-8
import requests, os, sys, time
from pathlib import Path
cwd = Path(__file__).resolve().parent
sys.path.append(str(cwd.parent))

from os import path, makedirs, getenv
from ddt.umamusume import get_live_list, lyrics_to_srt, select_dependencies


client = requests.Session()
client.proxies = {
    "http_proxy": getenv("HTTP_PROXY") or getenv("http_proxy") or None,
    "https_proxy": getenv("HTTPS_PROXY") or getenv("https_proxy") or None,
}
DOWNLOAD_PATH = path.join("downloads", "umamusume-live")


def download_stream(url: str, output: str) -> float:
    dura  = 0
    start = time.time()

    if not path.exists(path.dirname(output)):
        makedirs(path.dirname(output))
    if path.exists(output): return dura

    try:
        resp = client.get(url, stream=True)
        resp.raise_for_status()
        with open(output, "wb") as f:
            for chunk in resp.iter_content(chunk_size=64*1024):
                f.write(chunk)
    except Exception as e:
        print(f"failed to download {url}: {e}")
    else:
        end  = time.time()
        dura = end - start

    return dura


if __name__=="__main__":
    base = path.join(
        path.expanduser("~"),
        "AppData", "LocalLow", "Cygames", "umamusume"
    )
    flag_delete_base = False

    if not (os.path.exists(path.join(base, "meta")) and os.path.exists(path.join(base, "master", "master.mdb"))):
        import tempfile
        base = tempfile.mkdtemp()
        os.mkdir(os.path.join(base, "master"))
        flag_delete_base = True

        print("Game not installed, use meta/master.mdb from SimpleSandman/UmaMusumeMetaMasterMD!")
        dura = download_stream(url="https://raw.githubusercontent.com/SimpleSandman/UmaMusumeMetaMasterMDB/master/meta", output=os.path.join(base, "meta"))
        print(f"download meta in {dura:.2f}s")
        dura = download_stream(url="https://raw.githubusercontent.com/SimpleSandman/UmaMusumeMetaMasterMDB/master/master/master.mdb", output=os.path.join(base, "master", "master.mdb"))
        print(f"download master.mdb in {dura:.2f}s")
        print()


    try:
        live_dict = dict()
        live_list = get_live_list(umamusume_dir=base)
        for live in live_list:
            print(live)
            live_dict[str(live.music_id)] = live

        print()
        todo = input("Music ID: ").strip()

        if todo not in live_dict:
            print("Live not found!")
            exit(0)

        live = live_dict[todo]

        for blob in live.assets:

            if blob.type in ["sound"]: blob.path=path.join("sound", path.basename(blob.path))
            if "musicscores" in blob.path: blob.path=path.join("musicscores", path.basename(blob.path))

            output = path.join(DOWNLOAD_PATH, str(live), blob.path)
            dura = download_stream(blob.download_url, output)
            print(f"download {blob.path} in {dura:.2f}s")


        if path.exists(path.join(DOWNLOAD_PATH, str(live), "musicscores", f"m{todo}_lyrics")):
            if not path.exists(path.join(DOWNLOAD_PATH, str(live), "extract")):
                makedirs(path.join(DOWNLOAD_PATH, str(live), "extract"))

            lyrics_to_srt(
                path.join(DOWNLOAD_PATH, str(live), "musicscores", f"m{todo}_lyrics"),
                path.join(DOWNLOAD_PATH, str(live), "extract", f"m{todo}_lyrics.srt"),
            )

        if path.exists(path.join(DOWNLOAD_PATH, str(live), "live", "livesettings")):
            import UnityPy
            livesettings = None
            s = UnityPy.load(path.join(DOWNLOAD_PATH, str(live), "live", "livesettings"))
            assets = UnityPy.load(path.join(DOWNLOAD_PATH, str(live), "live", "livesettings")).assets[0]
            for (k, v) in assets.items():
                asset = v.read()
                if str(asset.name)==todo:
                    livesettings = asset

            if livesettings:
                controller_id = livesettings.text.split("\n")[2].split(",")[2]
                for blob in select_dependencies(base, f"3d/env/live/live{controller_id}/pfb_env_live{controller_id}_controller000"):
                    output = path.join(DOWNLOAD_PATH, str(live), blob.path)
                    dura = download_stream(blob.download_url, output)
                    print(f"download {blob.path} in {dura:.2f}s")

        print("\nAssets ✔️")

    except Exception as e:
        print(f"Fatal: {e}")
    finally:
        if flag_delete_base:
            import shutil
            shutil.rmtree(base)