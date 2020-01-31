from pynwb.behavior import BehavioralEvents

from src.datamigration.nwb_builder.managers.dio_manager import DioManager


class DioExtractor:

    def __init__(self, datasets, metadata):
        self.datasets = datasets
        self.dio_directories = datasets
        self.metadata = metadata
        self.all_dio_timeseries = metadata['behavioral_events']
        self.add_fields_to_dio(all_dio_timeseries=self.all_dio_timeseries)
        self.behavioral_event = BehavioralEvents(name='list of processed DIO`s', )
        self.dio_manager = DioManager(metadata=metadata)

    def get_dio(self):
        for dataset in self.datasets:
            self.create_timeseries(dataset=dataset,
                                   continuous_time_dict=DioManager.get_continuous_time_dict(dataset=dataset))
        return self.all_dio_timeseries

    def add_fields_to_dio(self, all_dio_timeseries):
        for series in all_dio_timeseries:
            series["dio_timeseries"] = []
            series["dio_timestamps"] = []

    def create_timeseries(self, continuous_time_dict, dataset):
        for dio_time_series in self.all_dio_timeseries:
            dio_data = self.dio_manager.get_extracted_dio(dataset=dataset, name=dio_time_series['name'])
            for recorded_event in dio_data['data']:
                self.create_timeseries_for_single_event(dio_time_series, recorded_event, continuous_time_dict)

    def create_timeseries_for_single_event(self, time_series, event, continuous_time_dict):
        time_series["dio_timeseries"].append(event[1])
        key = str(event[0])
        try:
            value = continuous_time_dict[key]
            time_series["dio_timestamps"].append(float(value) / 1E9)
        except KeyError:
            time_series["dio_timestamps"].append(float('nan'))
        return time_series
