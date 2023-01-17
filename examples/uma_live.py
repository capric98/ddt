#!/usr/bin/env python3
# coding: utf-8
import requests, sys, time
from pathlib import Path
cwd = Path(__file__).resolve().parent
sys.path.append(str(cwd.parent))

from os import path, makedirs, getenv
from ddt.umamusume import get_live_list


DOWNLOAD_PATH = path.join("env", "umamusume-live")


if __name__=="__main__":
    base = path.join(
        path.expanduser("~"),
        "AppData", "LocalLow", "Cygames", "umamusume"
    )

    live_dict = dict()
    live_list = get_live_list()
    for live in live_list:
        print(live)
        live_dict[str(live.music_id)] = live

    print()
    todo = input("Music ID: ").strip()

    if todo not in live_dict:
        print("Live not found!")
        exit(0)

    client = requests.Session()
    client.proxies = {
        "http_proxy": getenv("HTTP_PROXY") or getenv("http_proxy") or None,
        "https_proxy": getenv("HTTPS_PROXY") or getenv("https_proxy") or None,
    }

    live = live_dict[todo]

    for blob in live.assets:

        if blob.type in ["sound"]: blob.path=path.join("sound", path.basename(blob.path))
        if "musicscores" in blob.path: blob.path=path.join("musicscores", path.basename(blob.path))

        output = path.join(DOWNLOAD_PATH, str(live), blob.path)
        if not path.exists(path.dirname(output)):
            makedirs(path.dirname(output))
        if path.exists(output): continue

        start = time.time()
        try:
            resp = client.get(blob.download_url, stream=True)
            resp.raise_for_status()
            with open(output, "wb") as f:
                for chunk in resp.iter_content(chunk_size=64*1024):
                    f.write(chunk)
        except Exception as e:
            print(f"failed to download {blob.download_url}: {e}")
        else:
            end  = time.time()
            dura = end - start
            print(f"download {blob.path} in {dura:.2f}s")