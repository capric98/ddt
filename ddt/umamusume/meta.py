# coding: utf-8
import logging
from os import path
from dataclasses import dataclass
from typing import Generator

import sqlite3


_VERSION_TABLE_NAME  = "i"
_MANIFEST_TABLE_NAME = "a"


@dataclass
class UmaBlob:
    id  : int
    path: str
    hash: str
    def __str__(self) -> str:
        return "(UmaBlob) {} from [{}] {}".format(
            self.path,
            self.id, path.join("dat", self.hash[:2], self.hash)
        )
    def real_path(self, base: str) -> str:
        return path.join(base, "dat", self.hash[:2], self.hash)
    def download_url(self, endpoint: str="https://prd-storage-umamusume.akamaized.net"):
        pass


class UmaMeta():

    def __init__(self, base: str) -> None:
        self._base = base
        self._conn = sqlite3.connect(path.join(base, "meta"))

        version = self._conn.execute(f"SELECT * FROM {_VERSION_TABLE_NAME}")
        logging.info("opened meta database: {}".format(version.fetchone()))
        self._blobs = self._conn.execute(f"SELECT * FROM {_MANIFEST_TABLE_NAME}")
    def __del__(self) -> None:
        self._conn.close()

    def execute(self, query: str) -> sqlite3.Cursor:
        return self._conn.execute(query)

    def blobs(self) -> Generator[UmaBlob, None, None]:
        for row in self._blobs:
            blob_id   = row[0]
            blob_path = row[1]
            blob_hash = row[6]
            blob_type = row[7]

            if blob_path.startswith("//"):
                blob_path = path.join(blob_type, blob_path[2:])
            else:
                blob_path = path.join(blob_type, *(blob_path.split("/")))

            yield UmaBlob(blob_id, blob_path, blob_hash)


if __name__=="__main__":
    logging.basicConfig(level="INFO")

    base = path.join(
        path.expanduser("~"),
        "AppData", "LocalLow", "Cygames", "umamusume"
    )

    meta = UmaMeta(base)

    from os import makedirs
    import shutil
    for blob in meta.blobs():
        real_path = blob.real_path(base)
        output   = path.join("env", "umamusume-test", blob.path)
        if not path.exists(path.dirname(output)):
            makedirs(path.dirname(output))
        if path.exists(real_path) and not path.exists(output):
            logging.info(f"COPY {real_path} -> {output}")
            shutil.copyfile(real_path, output)
