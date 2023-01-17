# coding: utf-8
import logging
from os import path

import sqlite3

class UmaMaster:

    def __init__(self, base: str) -> None:
        self._base = base
        self._conn = sqlite3.connect(path.join(base, "master", "master.mdb"))
    def __del__(self) -> None:
        self._conn.close()

    def execute(self, query: str) -> sqlite3.Cursor:
        return self._conn.execute(query)
    def _dump_table(self, table: str) -> list[dict[str, any]]:
        results = []

        dumps = self.execute(f"SELECT * FROM {table}")
        names = [x[0] for x in dumps.description]

        for item in dumps:
            result = dict()

            for k in range(len(item)):
                result[names[k]] = item[k]

            results.append(result)

        return results

    @property
    def live_data(self, table: str="live_data") -> list[dict[str, any]]:
        return self._dump_table(table)
    @property
    def text_data(self, table: str="text_data") -> list[dict[str, any]]:
        return self._dump_table(table)


if __name__=="__main__":
    master = UmaMaster(base = path.join(
        path.expanduser("~"),
        "AppData", "LocalLow", "Cygames", "umamusume"
    ))

    print(master.live_data)
    print(master.text_data)