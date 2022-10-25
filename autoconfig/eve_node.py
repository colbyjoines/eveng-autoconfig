import re

class EveNode:
    node_types = {
        "vios-adventerprisek9-m": "Router",
        "i86bi_linux-adventerprisek9-ms": "Router",
        "l2": "Switch",
    }

    def __init__(self, node_data: dict) -> None:
        self.id = re.findall(r"\d+", node_data["name"])[0]
        self.name = node_data["name"]
        self.port = node_data["url"].split(":")[2]
        self.image = node_data["image"]
        self.node_type = self.get_node_type(node_data["image"])
        self.data = node_data

    def get_node_type(self, image: str):
        for key in self.node_types:
            if key in image:
                return self.node_types[key]
