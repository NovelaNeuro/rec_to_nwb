
class InvalidTimeInjector:

    @staticmethod
    def inject_mda_invalid_times(gaps, nwb_content):
        """insert electrical series to nwb file"""
        nwb_content.create_time_intervals(name='Valid Times',
                                          description='Some Description',
                                          )
        for gap in gaps:
            nwb_content.add_invalid_time_interval(start_time=gap[0], stop_time=gap[1])

