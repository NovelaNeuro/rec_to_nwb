from ndx_fllab_novela.apparatus import Node


class NodeCreator:

    @classmethod
    def create(cls, id, value):
        return Node(
            name='node' + str(id),
            value=value
        )
