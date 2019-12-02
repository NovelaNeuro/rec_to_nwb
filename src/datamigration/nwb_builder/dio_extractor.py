import datetime
import os

import numpy as np
import pandas as pd
import pynwb
from dateutil.tz import tzlocal
from pynwb import NWBFile, NWBHDF5IO, TimeSeries
from pynwb.behavior import BehavioralEvents
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

timestamp_list = []
pulses = []
for index in range(1, 33):
    d_in = readTrodesExtractedDataFile(
        'C:/Users/wmery/PycharmProjects/LorenFranksDataMigration/src/test/test_data/jaq/preprocessing/20190911/20190911_jaq_01_s1.DIO/20190911_jaq_01_s1.dio_Din' + str(index) + '.dat')
    for event_register in d_in['data']:
        timestamp_list.append(event_register[0])
        pulses.append(event_register[1])

print(timestamp_list)
print(pulses)


def add_behavioral_events(behavioral_timestamp, behavioral_data):
    return BehavioralEvents(name='behavioral name', time_series=TimeSeries(name='behavioral timeseries', data=behavioral_data, timestamps=behavioral_timestamp))



def build():

    content = NWBFile(session_description='self.metadata.session_description',
                                   experimenter='self.metadata.experimenter_name',
                                   lab='self.metadata.lab',
                                   institution='self.metadata.institution',
                                   session_start_time=datetime.datetime.strptime('10/31/2019 20:15:30',
                                                                                 '%m/%d/%Y %H:%M:%S'),
                                   identifier=str('self.metadata.identifier'),
                                   experiment_description='self.metadata.experiment_description'
                                   )

    content.create_processing_module(
        name='behaviour',
        description='Sample behaviour description'
    ).add_data_interface(
        add_behavioral_events(timestamp_list, pulses)
    )

    return content

with NWBHDF5IO('output_file.nwb', mode='w') as nwb_fileIO:
    nwb_fileIO.write(build())


with NWBHDF5IO('output_file.nwb', mode='r') as nwb_fileIO:
    print((nwb_fileIO.read().processing['behaviour']['behavioral name'].get_timeseries('behavioral timeseries').data))
