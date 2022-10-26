import networkx as nx
from networkx.algorithms.components.connected import connected_components

from .eve_api import EveApi
from .eve_node import EveNode


class EveTopology:
    def __init__(self, eve_config: dict, api: EveApi) -> None:
        self.segment_groups = []
        self.config = eve_config
        self.lab_path = eve_config["lab_path"]
        self.api = api
        self.nodes = self.get_nodes()
        self.links = self.get_links()
        self.graph = self.create_graph(self.nodes, self.links)
        self.l2_groups = self.find_l2(self.graph)
        self.graph = self.assign_l2_segments(self.graph, self.l2_groups)

    def get_nodes(self):
        result = {}
        nodes = self.api.get("/api/labs/" + self.lab_path + "/nodes").json()["data"]
        for key in nodes:
            result[nodes[key]["name"]] = EveNode(nodes[key], self.config)
        return result

    def get_links(self):
        return self.api.get("/api/labs/" + self.lab_path + "/topology").json()["data"]

    def create_graph(self, nodes, links):
        G = nx.Graph()
        G = self.add_nodes(nodes, G)
        G = self.add_links(links, G)
        return G

    def add_links(self, links, graph: nx.Graph):
        result = graph
        for link in links:
            result.add_edge(
                self.nodes[link["source_node_name"]],
                self.nodes[link["destination_node_name"]],
                object=link,
                links={
                    link["source_node_name"]: link["source_label"],
                    link["destination_node_name"]: link["destination_label"],
                },
            )
        return result

    def add_nodes(self, nodes, graph: nx.Graph):
        result = graph
        for node in nodes:
            result.add_node(nodes[node])
        return result

    def to_graph(self, l):
        G = nx.Graph()
        for part in l:
            G.add_nodes_from(part)
            G.add_edges_from(self.to_edges(part))
        return G

    def to_edges(self, l):
        it = iter(l)
        last = next(it)

        for current in it:
            yield last, current
            last = current

    def get_lowest_switch_id(self, group: list):
        ids = []
        for switch in group:
            ids.append(switch.id)
        return min(ids)

    def find_l2(self, graph: nx.Graph):
        result = []
        combined = self.combine_l2_switches(graph)

        for switch_group in combined:
            result.append(
                {"members": switch_group, "id": self.get_lowest_switch_id(switch_group)}
            )

        return result

    def combine_l2_switches(self, graph):
        combined = []
        for node in graph.nodes():
            switches = []
            if node.node_type == "Switch":
                switches.append(node)
                for adj_node in graph.adj[node]:
                    if adj_node.node_type == "Switch":
                        switches.append(adj_node)
                combined.append(switches)
        G = self.to_graph(combined)

        result = []
        for item in list(connected_components(G)):
            result.append(list(item))
        return result

    def search_l2_groups(self, node, l2_groups):
        result = False
        for group in l2_groups:
            for member in group["members"]:
                if member.id == node.id:
                    result = True

        return result

    def get_l2_group_id(self, node):
        result = 0
        for group in self.l2_groups:
            for member in group["members"]:
                if member.id == node.id:
                    result = group["id"]
                    break

        return result

    def assign_l2_segments(self, graph: nx.Graph, l2_groups: list):
        result = graph
        for edge in graph.edges():
            if edge[0].node_type == "Switch" and edge[1].node_type == "Switch":
                result[edge[0]][edge[1]]["type"] = "S2S"
            elif edge[0].node_type == "Router" and edge[1].node_type == "Router":
                result[edge[0]][edge[1]]["type"] = "R2R"
            elif edge[0].node_type == "Switch" and edge[1].node_type == "Router":
                result[edge[0]][edge[1]]["l2_group"] = self.get_l2_group_id(edge[0])
                result[edge[0]][edge[1]]["type"] = "R2S"
            elif edge[1].node_type == "Switch" and edge[0].node_type == "Router":
                result[edge[0]][edge[1]]["l2_group"] = self.get_l2_group_id(edge[1])
                result[edge[0]][edge[1]]["type"] = "R2S"
        return result

    @staticmethod
    def get_lowest_id(edge: tuple):
        if edge[0].id < edge[1].id:
            return edge[0].id
        else:
            return edge[1].id
