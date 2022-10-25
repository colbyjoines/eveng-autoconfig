import requests

class EveAuth:
    def __init__(self, eve_config: dict) -> None:
        self._config = eve_config
        self.auth = self.get_auth()
        self.cookies = self.auth.cookies

    def get_auth(self):
        return requests.post(
            "https://" + self._config["server"] + "/api/auth/login",
            verify=False,
            json={
                "username": self._config["username"],
                "password": self._config["password"],
                "html5": -1,
            },
        )
