class ValidTimeInjector:

    @staticmethod
    def inject_mda_valid_times(gaps, nwb_content):
        """insert electrical series to nwb file"""

        nwb_content.create_time_intervals(name='Valid Times',
                                          description='Some Description',
                                          columns=gaps
                                          )

