from pynwb import TimeSeries


class SampleCountTimestampCorespondenceBuilder:
    def __init__(self, data):
        self.data = data

    def build(self):
        return TimeSeries(name="SampleCountTimestampCorespondence",
                          description="Corespondence between sample count and timestamps",
                          data=self.data[0],
                          timestamps=self.data[1],
                          unit='int64'
                          )
