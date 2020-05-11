from rec_to_nwb.processing.nwb.components.apparatus.fl_apparatus import FlApparatus


class FlApparatusBuilder:

    @staticmethod
    def build(edges, nodes):
        return FlApparatus(edges, nodes)