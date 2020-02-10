import abc


class TimestampDataManager(abc.ABC):
    @abc.abstractmethod
    def read_data(self, dataset_num):
        pass

    @abc.abstractmethod
    def get_final_data_shape(self):
        pass
