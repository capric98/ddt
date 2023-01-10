#!/usr/bin/env python3
# coding: utf-8
import json, uuid

from .translator import EnhancedSession, Translator


class Caiyun(Translator):

    def __init__(self, token: str) -> None:
        super().__init__()

        self._endpoint = "https://api.interpreter.caiyunai.com/v1/translator"

        self._client = EnhancedSession()
        self._client.headers.update({
            "content-type": "application/json",
            "x-authorization": f"token {token}",
        })

    def interp(self, content: str | list[str], params=None) -> str | list[str]:
        if content=="": return content

        payload = {
            "source": content,
            "trans_type": "auto2zh",
            "request_id": "caiyun-"+str(uuid.uuid4()),
            "detect": True,
        }

        if params:
            for k in payload:
                if k in params:
                    payload[k] = params[k]

        resp = self._client.post(
            url  = self._endpoint,
            data = json.dumps(payload)
        )
        resp.raise_for_status()
        resp = resp.json()

        return resp["target"]


if __name__=="__main__":
    client = Caiyun(input("token: "))
    print(client.interp(["Lingocloud is the best translation service.", "彩云小译は最高の翻訳サービスです"]))