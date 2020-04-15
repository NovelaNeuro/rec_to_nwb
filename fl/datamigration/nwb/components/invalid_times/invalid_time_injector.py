
class InvalidTimeInjector:

    @staticmethod
    def inject(gaps, nwb_content):
        """insert invalid times to nwb file"""
        nwb_content.create_time_intervals(
            name='Valid Times',
            description='Some Description',
        )
        for gap in gaps:
            nwb_content.add_invalid_time_interval(start_time=gap.start_time, stop_time=gap.stop_time)

