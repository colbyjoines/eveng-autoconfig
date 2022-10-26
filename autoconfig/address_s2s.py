from .address import Address


class AddressS2S(Address):
    def __init__(self, graph, edge) -> None:
        self.graph = graph
        self.edge = edge

    def generate_address_v4(self):
        return {
            self.edge[0].name: {},
            self.edge[1].name: {},
        }