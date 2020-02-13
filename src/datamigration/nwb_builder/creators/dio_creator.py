from pynwb import TimeSeries


class DioCreator:
    @classmethod
    def create_dio_time_series(cls,behavioral_event, all_dio_time_series):
        for dio_time_series in all_dio_time_series:
            behavioral_event.add_timeseries(time_series=TimeSeries(name=dio_time_series['name'],
                                                                   data=dio_time_series["dio_timeseries"],
                                                                   timestamps=dio_time_series["dio_timestamps"],
                                                                   description=dio_time_series['description'],
                                                                   )
                                            )
        return behavioral_event
