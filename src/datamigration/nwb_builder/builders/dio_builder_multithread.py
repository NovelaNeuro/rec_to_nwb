import concurrent.futures

from src.datamigration.nwb_builder.extractors.continuous_time_extractor import ContinuousTimeExtractor
from src.datamigration.nwb_builder.extractors.dio_extractor import DioExtractor
from src.datamigration.nwb_builder.managers.dio_manager import DioManager


# change the name of this file if its working correctly
class DioBuilder:
    def __init__(self, datasets, metadata):
        self.datasets = datasets
        self.metadata = metadata
        self.continuous_time_extractor = ContinuousTimeExtractor()
        self.dio_manager = DioManager(datasets, metadata)
        self.filtered_dio_files = DioManager.get_dio_files()

    def build_dio(self):
        all_dio_data = []
        threads = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in range(len(self.datasets)):
                extractor = DioExtractor(filtered_dataset_dio_files=self.filtered_dio_files[i],
                                         dio_metadata=self.metadata,
                                         continuous_time_dict=self.continuous_time_extractor.get_continuous_time_dict_file(
                                             self.datasets[i].get_continuous_time()
                                         ))
                threads.append(executor.submit(extractor.get_dio()))
        for i in range(len(self.datasets)):
            all_dio_data.extend(threads[i].result())
