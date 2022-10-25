import requests
import json

from .eve_auth import EveAuth
import requests


class EveApi:
    def __init__(self, eve_config: dict, eve_auth: EveAuth) -> None:
        self.config = eve_config
        self.auth = eve_auth
        self.cookies = eve_auth.cookies

    def get(self, uri: str):
        return requests.get(
            url="https://" + self.config["server"] + uri,
            verify=False,
            headers={"Content-type": "application/json"},
            cookies=self.cookies,
        )

    def post(self, uri: str, body: dict):
        return requests.post(
            "https://" + self.config["server"] + uri,
            verify=False,
            json=body,
        )
