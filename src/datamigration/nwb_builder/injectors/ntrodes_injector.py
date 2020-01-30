class NTrodesInjector:
    def inject_ntrode(self, nwb_content, ntrode):
        nwb_content.add_electrode_group(ntrode)
