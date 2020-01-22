from src.datamigration.nwb_builder.electrode_extractor import ElectrodeExtractor


class ElectrodeTableBuilder:
    def __init__(self, nwb_file_content, probes, electrode_groups, header):
        self.nwb_file_content = nwb_file_content
        self.electrode_groups = electrode_groups
        self.electrode_extractor = ElectrodeExtractor(probes=probes, header=header)
        self.electrodes = self.get_data_from_ymls()
        self.add_electrodes()
        self.add_all_electrode_properties()

    def get_data_from_ymls(self):
        return self.electrode_extractor.get_all_electrodes()

    def add_electrode_property(self, new_column_name,
                               data_for_existing_electrodes, column_description='No description'):
        self.nwb_file_content.electrodes.add_column(
            name=new_column_name,
            description=column_description,
            data=data_for_existing_electrodes
        )

    def add_all_electrode_properties(self):
        base_properties = ["x", "y", "z", "imp", "location", "filtering", "electrode_group", "id"]
        new_properties = []
        keys = self.electrodes[0].keys()
        for key in keys:
            if key not in base_properties:
                new_properties.append(key)
        for new_property in new_properties:
            data = [electrode[new_property] for electrode in self.electrodes]
            self.add_electrode_property(new_property, data)

    def add_electrodes(self):
        current_id = 0
        for electrode in self.electrodes:
            self.nwb_file_content.add_electrode(
                x=0.0,
                y=0.0,
                z=0.0,
                imp=1.0,
                location='necessary location',
                filtering="have no idea",
                group=self.electrode_groups['electrode group ' + str(electrode["electrode_group"])],
                id=current_id)
        current_id += 1
