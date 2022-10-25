import networkx as nx

from .eve_api import EveApi
from .eve_node import EveNode


class EveTopology:
    def __init__(self, lab_path: str, api: EveApi) -> None:
        self.segment_groups = []
        self._lab_path = lab_path
        self._api = api
        self.nodes = self.get_nodes()
        self._links = self.get_links()
        self.graph = self.create_graph(self.nodes, self._links)
        self.l2_groups = self.find_l2(self.graph)
        self.graph = self.assign_l2_segments(self.graph, self.l2_groups)

    def get_nodes(self):
        result = {}
        nodes = self._api.get("/api/labs/" + self._lab_path + "/nodes").json()["data"]
        for key in nodes:
            result[nodes[key]["name"]] = EveNode(nodes[key])
        return result

    def get_links(self):
        return self._api.get("/api/labs/" + self._lab_path + "/topology").json()["data"]

    def create_graph(self, nodes, links):
        G = nx.Graph()

        for node in nodes:
            G.add_node(nodes[node])

        for link in links:
            G.add_edge(
                self.nodes[link["source_node_name"]],
                self.nodes[link["destination_node_name"]],
                object=link,
                links={
                    link["source_node_name"]: link["source_label"],
                    link["destination_node_name"]: link["destination_label"],
                },
            )

        return G

    def find_l2(self, graph: nx.Graph):
        result = []
        for edge in graph.edges():
            if edge[0].node_type == "Switch" and edge[1].node_type == "Switch":
                result.append(
                    {
                        "members": [edge[0], edge[1]],
                        "id": self.get_lowest_id(edge),
                    }
                )

        for node in graph.nodes():
            if node.node_type == "Switch":
                if self.search_l2_groups(node, result) == False:
                    result.append({"members": [node], "id": node.id})

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

        return result

    @staticmethod
    def get_lowest_id(edge: tuple):
        if edge[0].id < edge[1].id:
            return edge[0].id
        else:
            return edge[1].id

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
