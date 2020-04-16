
class InvalidTimeInjector:

    @staticmethod
    def inject(gaps, nwb_content):
        """insert invalid times to nwb file"""
        nwb_content.create_time_intervals(
            name='Invalid Times',
            description='Invalid times based on mda timestamps',
        )
        for gap in gaps:
            nwb_content.add_invalid_time_interval(start_time=gap.start_time, stop_time=gap.stop_time)

