import requests

class EveAuth:
    def __init__(self, eve_config: dict) -> None:
        self.config = eve_config
        self.auth = self.get_auth()
        self.cookies = self.auth.cookies

    def get_auth(self):
        return requests.post(
            "https://" + self.config["server"] + "/api/auth/login",
            verify=False,
            json={
                "username": self.config["username"],
                "password": self.config["password"],
                "html5": -1,
            },
        )
