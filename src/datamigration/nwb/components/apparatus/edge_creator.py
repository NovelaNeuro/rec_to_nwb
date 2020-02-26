from ndx_franklab_novela.apparatus import Edge


class EdgeCreator:

    @classmethod
    def create(cls, id, edge_nodes):
        return Edge(
            name='edge' + str(id),
            edge_nodes=edge_nodes
        )