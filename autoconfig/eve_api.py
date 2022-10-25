import requests
import json

from eveng_autoconfig.eve_auth import EveAuth
import requests


class EveApi:
    def __init__(self, eve_config: dict, eve_auth: EveAuth) -> None:
        self._config = eve_config
        self._auth = eve_auth
        self._cookies = eve_auth.cookies

    def get(self, uri: str):
        return requests.get(
            url="https://" + self._config["server"] + uri,
            verify=False,
            headers={"Content-type": "application/json"},
            cookies=self._cookies,
        )

    def post(self, uri: str, body: dict):
        return requests.post(
            "https://" + self._config["server"] + uri,
            verify=False,
            json=body,
        )
