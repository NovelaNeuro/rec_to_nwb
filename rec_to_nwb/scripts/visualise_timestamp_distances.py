from pathlib import Path

from mountainlab_pytools.mdaio import readmda
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from rec_to_nwb.processing.metadata.metadata_manager import MetadataManager
from rec_to_nwb.processing.time.continuous_time_extractor import ContinuousTimeExtractor
from rec_to_nwb.processing.time.timestamp_converter import TimestampConverter

from matplotlib import pyplot
import pandas as pd

from rec_to_nwb.processing.tools.data_scanner import DataScanner

path = Path(__file__).parent.parent
path.resolve()


def read_mda_timestamps(file):
    return readmda(file)

def read_pos_timestamps(file):
    pos_online = readTrodesExtractedDataFile(file)
    position = pd.DataFrame(pos_online['data'])
    return position.time.to_numpy(dtype='int64')

def get_posonline_data_file(dataset):
    all_pos = dataset.get_all_data_from_dataset('pos')
    for pos_file in all_pos:
        if pos_file.endswith('pos_online.dat'):
            return dataset.get_data_path_from_dataset('pos') + pos_file
    return None

def extract_datasets(data_scanner, animal_name, date):
    data_scanner.extract_data_from_date_folder(date)
    dataset_names = data_scanner.get_all_epochs(date)
    return[data_scanner.data[animal_name][date][dataset] for dataset in dataset_names]

if __name__ == "__main__":
    animal_name = 'beans'
    date = '20190718'
    data_path = 'C:/Users/wbodo/Desktop/resy/test/'
    # data_path = str(path) + '/test/test_data/'
    nwb_metadata = MetadataManager(
        str(path) + '/test/processing/res/metadata.yml',
        [str(path) + '/test/processing/res/probe1.yml',
         str(path) + '/test/processing/res/probe2.yml',
         str(path) + '/test/processing/res/probe3.yml']
    )
    data_scanner = DataScanner(data_path, animal_name, nwb_metadata)
    datasets = extract_datasets(data_scanner, animal_name, date)

    pos_timestamps_files = [get_posonline_data_file(dataset) for dataset in datasets]
    mda_timestamps_files = [dataset.get_mda_timestamps() for dataset in datasets]
    continuous_time_files = [dataset.get_continuous_time() for dataset in datasets]

    timestamps = [read_pos_timestamps(timestamps_file) for timestamps_file in pos_timestamps_files]
    continuous_time_extractor = ContinuousTimeExtractor()
    continuous_time_dicts = continuous_time_extractor.get_continuous_time_dict(continuous_time_files)

    distances = []
    max_distance = 0
    for i, continuous_time_dict in enumerate(continuous_time_dicts):
        converted_timestamps = TimestampConverter.convert_timestamps(continuous_time_dict, timestamps[i])
        for j in range(1, len(converted_timestamps) -1):
            if converted_timestamps[j] > 0 and converted_timestamps[j - 1] > 0:
                new_dist = (converted_timestamps[j] - converted_timestamps[j - 1])
                if new_dist > max_distance:
                    max_distance = new_dist

                distances.append(new_dist)

    pyplot.hist(distances, bins=500, range=(0, max_distance))
    pyplot.show()

    timestamps = [read_mda_timestamps(timestamps_file) for timestamps_file in mda_timestamps_files]

    for i, continuous_time_dict in enumerate(continuous_time_dicts):
        converted_timestamps = TimestampConverter.convert_timestamps(continuous_time_dict, timestamps[i])
        for j in range(1, len(converted_timestamps) -1):
            if converted_timestamps[j] > 0 and converted_timestamps[j - 1] > 0:
                new_dist = (converted_timestamps[j] - converted_timestamps[j - 1])
                if new_dist > max_distance:
                    max_distance = new_dist

                distances.append(new_dist)

    pyplot.hist(distances, bins=4000, range=(0, max_distance))
    pyplot.show()
