from .eve_topology import EveTopology


class Address:
    def __init__(self) -> None:
        pass

    def generate_address_v4(self):
        return {self.edge[0].name: {}, self.edge[1].name: {}}

    def generate_address_v6(self):
        return {self.edge[0].name: {}, self.edge[1].name: {}}

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

    def get_link_id_v6(self, edge: tuple):
        result = ""
        lowest = EveTopology.get_lowest_id(edge)
        if edge[0].id == lowest:
            result = str(lowest + edge[1].id)
        else:
            result = str(edge[1].id + lowest)

        if len(result) == 2:
            result = "0" + result
        elif len(result) == 3:
            result = "0" + result[0] + result[-2] + result[-1]
            
        return result
