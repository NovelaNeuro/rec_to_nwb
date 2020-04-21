from ndx_fl_novela.apparatus import Node


class NodeCreator:

    @classmethod
    def create(cls, id, value):
        return Node(
            name='node' + str(id),
            value=value
        )
