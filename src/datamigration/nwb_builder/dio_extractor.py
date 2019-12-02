import datetime
import os

import numpy as np
import pandas as pd
import pynwb
from dateutil.tz import tzlocal
from pynwb import NWBFile, NWBHDF5IO, TimeSeries
from pynwb.behavior import BehavioralEvents
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

d_in = readTrodesExtractedDataFile(
    'C:/Users/wmery/PycharmProjects/LorenFranksDataMigration/src/test/test_data/jaq/preprocessing/20190911/20190911_jaq_01_s1.DIO/20190911_jaq_01_s1.dio_Din1.dat')
d_in1 = pd.DataFrame(d_in['data'])
print(d_in1)
# st = datetime.datetime(20, 5, 5, tzinfo=tzlocal())
#
# def build(session_start_time, dio):
#
#     content = NWBFile(session_description='self.metadata.session_description',
#                                    experimenter='self.metadata.experimenter_name',
#                                    lab='self.metadata.lab',
#                                    institution='self.metadata.institution',
#                                    session_start_time=session_start_time,
#                                    identifier=str('self.metadata.identifier'),
#                                    experiment_description='self.metadata.experiment_description'
#                                    )
#
#     ts = TimeSeries(name='behavioral_events_name', source='behavioral_events_source',
#                     data=dio['data'],
#                     timestamps=dio['timestamp_at_creation'],
#                     )
#
#     behavioral_events = BehavioralEvents(time_series=ts, name='BehavioralEvents_name')
#     behavioral_events.add_timeseries(ts)
#
#
#     return content
#
# with NWBHDF5IO('output_file', mode='w') as nwb_fileIO:
#     nwb_fileIO.write(build(st, d_in))
#     nwb_fileIO.close()
