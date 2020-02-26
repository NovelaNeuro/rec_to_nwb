from src.datamigration.nwb.components.apparatus.edge_creator import EdgeCreator
from src.datamigration.nwb.components.apparatus.node_creator import NodeCreator


class LfApparatusExtractor:
    def __init__(self, apparatus_metadata):
        self.apparatus_metadata = apparatus_metadata
        self.node_creator = NodeCreator()
        self.edge_creator = EdgeCreator()

    def get_data(self):
        nodes = []
        edges = []
        col_nodes = []
        global_counter = 0
        
        for row_counter, row in enumerate(self.apparatus_metadata):
            for col in row:
                col_nodes.append(self.node_creator.create(global_counter, col))
                global_counter = global_counter + 1

            nodes.extend(col_nodes)
            edges.append(self.edge_creator.create(row_counter, col_nodes))
            col_nodes = []
        return edges, nodes
