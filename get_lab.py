import requests
import json


def get_nodes(cookies):

    with open("config.json") as json_file:
        data = json.load(json_file)
    return requests.get(
        url="https://" + data["server"] + "/api/labs/" + data["lab_path"] + "/nodes",
        verify=False,
        headers={"Content-type": "application/json"},
        cookies=cookies,
    ).json()["data"]


def get_topology(cookies):

    with open("config.json") as json_file:
        data = json.load(json_file)
    return requests.get(
        url="https://" + data["server"] + "/api/labs/" + data["lab_path"] + "/topology",
        verify=False,
        headers={"Content-type": "application/json"},
        cookies=cookies,
    ).json()["data"]
