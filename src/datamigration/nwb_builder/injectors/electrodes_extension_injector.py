class ElectrodesExtensionInjector:
    @staticmethod
    def inject_extensions(nwb_content, electrodes_metadata_extension, electrodes_header_extension):
        nwb_content.electrodes.add_column(
            name='hwChan',
            description='None',
            data=electrodes_header_extension
        )

        nwb_content.electrodes.add_column(
            name='rel_x',
            description='None',
            data=electrodes_metadata_extension.rel_x
        )

        nwb_content.electrodes.add_column(
            name='rel_y',
            description='None',
            data=electrodes_metadata_extension.rel_y
        )

        nwb_content.electrodes.add_column(
            name='rel_z',
            description='None',
            data=electrodes_metadata_extension.rel_z
        )

