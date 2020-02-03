class NTrodesInjector:
    @staticmethod
    def inject_ntrode(nwb_content, ntrode):
        nwb_content.add_electrode_group(ntrode)
