from pynwb import TimeSeries


class SampleCountTimestampCorespondenceBuilder:
    def __init__(self, data):
        self.data = data

    def build(self):
        return TimeSeries(name="sample_count",
                          description="acquisition system sample count",
                          data=self.data[:, 0],
                          timestamps=self.data[:, 1],
                          unit='int64'
                          )
