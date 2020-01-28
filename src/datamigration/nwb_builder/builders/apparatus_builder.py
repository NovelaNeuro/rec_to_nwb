from src.datamigration.extension.apparatus import Apparatus
from src.datamigration.extension.edge import Edge
from src.datamigration.extension.node import Node


def build_apparatus(metadata, nwb_content):
    nodes = []
    edges = []
    col_nodes = []
    global_counter = 0
    for row_counter, row in enumerate(metadata['apparatus']['data']):
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

    nwb_content.processing["behavior"].add_data_interface(
        Apparatus(
            name='apparatus',
            edges=edges,
            nodes=nodes
        )
    )