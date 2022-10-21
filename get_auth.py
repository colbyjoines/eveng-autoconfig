import requests
import json


def get_auth():

    with open("config.json") as json_file:
        data = json.load(json_file)

    return requests.post(
        "https://" + data["server"] + "/api/auth/login",
        verify=False,
        json={"username": data["username"], "password": data["password"], "html5": -1},
    )
