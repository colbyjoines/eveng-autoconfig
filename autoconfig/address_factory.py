import networkx as nx

from .address_r2r import AddressR2R
from .address_r2s import AddressR2S
from .address_s2s import AddressS2S

class AddressFactory:
    def __init__(self, graph: nx.Graph) -> None:
        self.graph = graph
    
    def make(self, edge: tuple):
        if self.graph[edge[0]][edge[1]]["type"] == "S2S":
            return AddressS2S(self.graph, edge)
        if self.graph[edge[0]][edge[1]]["type"] == "R2R":
            return AddressR2R(self.graph, edge) 
        if self.graph[edge[0]][edge[1]]["type"] == "R2S":
            return AddressR2S(self.graph, edge) 