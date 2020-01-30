from src.datamigration.extension.edge import Edge
from src.datamigration.extension.node import Node


class ApparatusExtractor:
    def __init__(self, metadata):
        self.metadata = metadata

    def get_data(self):
        nodes = []
        edges = []
        col_nodes = []
        global_counter = 0
        for row_counter, row in enumerate(self.metadata['apparatus']['data']):
            for col_counter, col in enumerate(row):
                col_nodes.append(
                    Node(
                        name='node' + str(global_counter),
                        value=col
                    )
                )
                global_counter = global_counter + 1

            nodes.extend(col_nodes)
            edges.append(
                Edge(
                    name='edge' + str(row_counter),
                    edge_nodes=col_nodes
                )
            )
            col_nodes = []
        return edges, nodes