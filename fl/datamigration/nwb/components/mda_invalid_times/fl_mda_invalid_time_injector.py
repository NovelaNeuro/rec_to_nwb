
class MdaInvalidTimeInjector:

    @staticmethod
    def inject_all(gaps, nwb_content):
        """insert invalid times to nwb file"""
        nwb_content.create_time_intervals(
            name='Mda Invalid Times',
            description='Invalid times based on mda timestamps',
        )
        for gap in gaps:
            MdaInvalidTimeInjector.inject(gap, nwb_content)

    @staticmethod
    def inject(gap, nwb_content):
        nwb_content.add_invalid_time_interval(
            start_time=gap.start_time,
            stop_time=gap.stop_time
        )


