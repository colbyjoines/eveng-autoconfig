from os import link
from pprint import pprint
import networkx as nx

from .eve_topology import EveTopology
from .address_factory import AddressFactory


class GenerateIpAddressing:
    def __init__(self, config: dict, graph: nx.Graph):
        self.config = config
        self.graph = graph
        self.addressing = {}

    def generate_physical(self):
        for node in self.graph.nodes():
            self.addressing[node.name] = []

        for edge in self.graph.edges():
            address_config = AddressFactory(self.graph).make(edge)
            ipv4 = address_config.generate_address_v4()
            ipv6 = address_config.generate_address_v6()
            self.addressing[edge[0].name].append(ipv4[edge[0].name])
            self.addressing[edge[1].name].append(ipv4[edge[1].name])
            self.addressing[edge[0].name].append(ipv6[edge[0].name])
            self.addressing[edge[1].name].append(ipv6[edge[1].name])

        print(self.addressing)

    def generate_loopbacks(self):
        for node in self.graph.nodes():
            if node.node_type == "Router":
                for loopback in range(
                    0, self.config["config_options"]["loopback_count"]
                ):
                    self.addressing[node.name].append(
                        {
                            "interface": f"loopback{loopback}",
                            "address": node.id + f"0.100.{str(loopback)}.1",
                            "mask": "255.255.255.0",
                            "type": "ipv4",
                            "additional_config": ["ip ospf network point-to-point"],
                        }
                    )
                    self.addressing[node.name].append(
                        {
                            "interface": f"loopback{str(loopback + 10)}",
                            "address": "100.1." + node.id + f".{str(loopback)}",
                            "mask": "255.255.255.255",
                            "type": "ipv4",
                            "additional_config": [],
                        }
                    )
                    if (
                        node.name
                        in self.config["config_options"]["add_duplicate_loopbacks"]
                    ):
                        loopback = str(loopback + 20)
                        self.addressing[node.name].append(
                            {
                                "interface": f"loopback{loopback}",
                                "address": f"1.1.1.{loopback}",
                                "mask": "255.255.255.255",
                                "type": "ipv4",
                                "additional_config": [],
                            }
                        )
