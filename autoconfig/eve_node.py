import re


class EveNode:
    def __init__(self, node_data: dict, eve_config: dict) -> None:
        self.config = eve_config
        self.id = re.findall(r"\d+", node_data["name"])[0]
        self.name = node_data["name"]
        self.port = node_data["url"].split(":")[2]
        self.image = node_data["image"]
        self.node_type = self.get_node_type(node_data["image"])
        self.data = node_data

    def get_node_type(self, image: str):
        for key in self.config["images"]:
            if key in image:
                return self.config["images"][key]
