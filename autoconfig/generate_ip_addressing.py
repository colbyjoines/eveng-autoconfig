from os import link
from pprint import pprint
import networkx as nx

from .eve_topology import EveTopology


class GenerateIpAddressing:
    def __init__(self, config: dict, graph: nx.Graph):
        self.config = config
        self.graph = graph
        self.addressing = {}
        for node in self.graph.nodes():
            self.addressing[node.name] = []
        self.generate_physical()
        self.generate_loopbacks()

    def generate_physical(self):
        for edge in self.graph.edges():
            if self.graph[edge[0]][edge[1]]["type"] == "S2S":
                continue
            if self.graph[edge[0]][edge[1]]["type"] == "R2R":
                link_id = self.get_link_id(edge)
                self.addressing[edge[0].name].append(
                    {
                        "interface": self.graph[edge[0]][edge[1]]["links"][
                            edge[0].name
                        ],
                        "address": f"10.0.{link_id}." + edge[0].id,
                        "mask": "255.255.255.0",
                        "additional_config": [],
                    }
                )
                self.addressing[edge[1].name].append(
                    {
                        "interface": self.graph[edge[0]][edge[1]]["links"][
                            edge[1].name
                        ],
                        "address": f"10.0.{link_id}." + edge[1].id,
                        "mask": "255.255.255.0",
                        "additional_config": [],
                    }
                )
            elif edge[0].node_type == "Switch" and edge[1].node_type == "Router":
                l2_id = self.graph[edge[0]][edge[1]]["l2_group"]
                self.addressing[edge[1].name].append(
                    {
                        "interface": self.graph[edge[0]][edge[1]]["links"][
                            edge[1].name
                        ],
                        "address": f"10.{l2_id}.{l2_id}." + edge[1].id,
                        "mask": "255.255.255.0",
                        "additional_config": [],
                    }
                )
            else:
                l2_id = self.graph[edge[1]][edge[0]]["l2_group"]
                self.addressing[edge[0].name].append(
                    {
                        "interface": self.graph[edge[0]][edge[1]]["links"][
                            edge[0].name
                        ],
                        "address": f"10.{l2_id}.{l2_id}." + edge[0].id,
                        "mask": "255.255.255.0",
                        "additional_config": [],
                    }
                )
        pprint(self.addressing, indent=4)
        # exit()
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
                            "additional_config": ["ip ospf network point-to-point"],
                        }
                    )
                    self.addressing[node.name].append(
                        {
                            "interface": f"loopback{str(loopback + 10)}",
                            "address": "100.1." + node.id + f".{str(loopback)}",
                            "mask": "255.255.255.255",
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
                                "additional_config": [],
                            }
                        )

    def get_link_id(self, edge: tuple):
        result = ""
        lowest = EveTopology.get_lowest_id(edge)
        if edge[0].id == lowest:
            result = str(lowest + edge[1].id)
        else:
            result = str(edge[1].id + lowest)
            
        if len(result) > 3:
            result = result[0] + result[-2] + result[-1]
        return result
