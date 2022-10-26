from .address import Address


class AddressR2S(Address):
    def __init__(self, graph, edge) -> None:
        self.graph = graph
        self.edge = edge
        self.mask = "255.255.255.0"
        self.prefix = "10.0."

    def generate_address_v4(self):
        result = {
            self.edge[0].name: {},
            self.edge[1].name: {}
        }
        if self.edge[0].node_type == "Switch" and self.edge[1].node_type == "Router":
            l2_id = self.graph[self.edge[0]][self.edge[1]]["l2_group"]
            result[self.edge[1].name] = {
                "interface": self.graph[self.edge[0]][self.edge[1]]["links"][self.edge[1].name],
                "address": f"10.{l2_id}.{l2_id}." + self.edge[1].id,
                "mask": self.mask,
                "type": "ipv4",
                "additional_config": [],
            }

        else:
            l2_id = self.graph[self.edge[1]][self.edge[0]]["l2_group"]
            result[self.edge[0].name] = {
                "interface": self.graph[self.edge[0]][self.edge[1]]["links"][self.edge[0].name],
                "address": f"10.{l2_id}.{l2_id}." + self.edge[0].id,
                "mask": self.mask,
                "type": "ipv4",
                "additional_config": [],
            }

        return result
    
    def generate_address_v6(self):
        result = {
            self.edge[0].name: {},
            self.edge[1].name: {}
        }
        if self.edge[0].node_type == "Switch" and self.edge[1].node_type == "Router":
            l2_id = self.graph[self.edge[0]][self.edge[1]]["l2_group"]
            result[self.edge[1].name]["interface"] = self.graph[self.edge[0]][self.edge[1]]["links"][self.edge[1].name]
            result[self.edge[1].name]["address"] = f"2001:0:{l2_id}:{l2_id}::" + self.edge[1].id
            result[self.edge[1].name]["mask"] = "/64"
            result[self.edge[1].name]["type"] = "ipv6"
            result[self.edge[1].name]["additional_config"] = []

        else:
            l2_id = self.graph[self.edge[1]][self.edge[0]]["l2_group"]
            result[self.edge[0].name]["interface"] = self.graph[self.edge[0]][self.edge[1]]["links"][self.edge[0].name]
            result[self.edge[0].name]["address"] = f"2001:0:{l2_id}:{l2_id}::" + self.edge[0].id
            result[self.edge[0].name]["mask"] = "/64"
            result[self.edge[0].name]["type"] = "ipv6"
            result[self.edge[0].name]["additional_config"] = []
           
        return result
