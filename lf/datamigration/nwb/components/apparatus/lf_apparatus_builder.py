from lf.datamigration.nwb.components.apparatus.lf_apparatus import LfApparatus


class LfApparatusBuilder:

    @staticmethod
    def build(edges, nodes):
        return LfApparatus(edges, nodes)