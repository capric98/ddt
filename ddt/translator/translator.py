# coding: utf-8
import requests


class EnhancedSession(requests.Session):
    def __init__(self, timeout=(5, 10)):
        self._timeout = timeout
        return super().__init__()

    def request(self, method, url, **kwargs):
        # print("EnhancedSession request")
        if "timeout" not in kwargs:
            kwargs["timeout"] = self._timeout
        return super().request(method, url, **kwargs)


class Translator:
    def interp(self, content: str | list[str], params=None) -> str | list[str]:
        pass