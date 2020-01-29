from src.datamigration.extension.apparatus import Apparatus
from src.datamigration.extension.edge import Edge
from src.datamigration.extension.node import Node


class ApparatusBuilder:

    def __init__(self, metadata, nwb_content):
        self.metadata = metadata
        self.nwb_content = nwb_content
        self.nodes = []
        self.edges = []

    def build(self):
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

            self.nodes.extend(col_nodes)
            self.edges.append(
                Edge(
                    name='edge' + str(row_counter),
                    edge_nodes=col_nodes
                )
            )
            col_nodes = []

        return Apparatus(
                        name='apparatus',
                        edges=self.edges,
                        nodes=self.nodes
                        )
