class Electrodes():
    def __init__(self, nwb_file_content, metadata):
        self.nwb_file_content = nwb_file_content
        self.metadata = metadata

    def get_data_from_metadata(self, property_name):
        print("whtvr")

    def add_electrode_property(self, new_column_name,
                               data_for_existing_electrodes=[], column_description='No description'):
        data = [i for i in range(len(self.metadata.electrodes))]
        self.nwb_file_content.electrodes.add_column(
            name=new_column_name,
            description=column_description,
            data=data
        )

    def add_electrodes(self):
        for electrode in self.metadata.electrodes:
            self.nwb_file_content.add_electrode(
                x=electrode['x'],
                y=electrode['y'],
                z=electrode['z'],
                imp=1.0,
                location='necessary location',
                filtering=electrode['filtering'],
                group=self.nwb_file_content.electrode_groups['1'],
                id=electrode['id'],
            )
