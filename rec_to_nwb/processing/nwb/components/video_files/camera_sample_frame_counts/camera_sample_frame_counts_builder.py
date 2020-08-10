from pynwb import TimeSeries


class CameraSampleFrameCountsBuilder:
    def __init__(self, data):
        self.data = data

    def build(self):
        return self.__build_timeseries(self.data)

    @classmethod
    def __build_timeseries(cls, data):
        return TimeSeries(name="CameraSampleFrameCounts",
                          description="Camera sample frame counts",
                          data=data.frame_count,
                          timestamps=data.timestamps
                          )
