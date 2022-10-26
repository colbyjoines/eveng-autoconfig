from .address import Address


class AddressR2R(Address):
    def __init__(self, graph, edge) -> None:
        self.graph = graph
        self.edge = edge
        self.mask = "255.255.255.0"
        self.prefix = "10.0."

    def generate_address_v4(self):
        link_id = self.get_link_id(self.edge)
        
        result = {
            self.edge[0].name: {},
            self.edge[1].name: {},
        }
        result[self.edge[0].name]["interface"] = self.graph[self.edge[0]][self.edge[1]]["links"][self.edge[0].name]
        result[self.edge[0].name]["address"] = self.prefix + link_id + "." + self.edge[0].id
        result[self.edge[0].name]["mask"] = self.mask
        result[self.edge[0].name]["type"] = "ipv4"
        result[self.edge[0].name]["additional_config"] = []
        result[self.edge[1].name]["interface"] = self.graph[self.edge[0]][self.edge[1]]["links"][self.edge[1].name]
        result[self.edge[1].name]["address"] = self.prefix + link_id + "." + self.edge[1].id
        result[self.edge[1].name]["mask"] = self.mask
        result[self.edge[1].name]["type"] = "ipv4"
        result[self.edge[1].name]["additional_config"] = []
        
        return result
    
    def generate_address_v6(self):
        link_id = self.get_link_id(self.edge)
        
        result = {
            self.edge[0].name: {},
            self.edge[1].name: {},
        }
        result[self.edge[0].name]["interface"] = self.graph[self.edge[0]][self.edge[1]]["links"][self.edge[0].name]
        result[self.edge[0].name]["address"] = "2001:0:0:" + link_id + "::" + self.edge[0].id
        result[self.edge[0].name]["mask"] = "/64"
        result[self.edge[0].name]["type"] = "ipv6"
        result[self.edge[0].name]["additional_config"] = []
        result[self.edge[1].name]["interface"] = self.graph[self.edge[0]][self.edge[1]]["links"][self.edge[1].name]
        result[self.edge[1].name]["address"] = "2001:0:0:" + link_id + "::" + self.edge[1].id
        result[self.edge[1].name]["mask"] = "/64"
        result[self.edge[1].name]["type"] = "ipv6"
        result[self.edge[1].name]["additional_config"] = []
        
        return result
