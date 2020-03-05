from fl.datamigration.nwb.components.apparatus.fl_apparatus import LfApparatus


class LfApparatusBuilder:

    @staticmethod
    def build(edges, nodes):
        return LfApparatus(edges, nodes)