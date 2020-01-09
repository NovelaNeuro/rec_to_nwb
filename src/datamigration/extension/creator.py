from dateutil.tz import tzlocal
from pynwb import NWBHDF5IO, NWBFile
from datetime import datetime

from pynwb.device import Device

from src.datamigration.extension.probe import Probe

start_time = datetime(2017, 4, 3, 11, tzinfo=tzlocal())

content = NWBFile(session_description='self.metadata.session_description',
                  experimenter='self.metadata.experimenter_name',
                  lab='self.metadata.lab',
                  institution='self.metadata.institution',
                  session_start_time=start_time,
                  identifier=str('self.metadata.identifier'),
                  experiment_description='self.metadata.experiment_description',
                  devices=[Device(name='trodes')]
                  )
devices = [Device(name='n1'), Device(name='n2')]
probe = Probe(name='somename', devices=devices, location='l1', description='d1', device=content.devices['trodes'], id=1)
print(probe.devices)
content.add_electrode_group(probe)
print(content.electrode_groups['somename'])
with NWBHDF5IO(path='output_file.nwb', mode='w') as nwb_fileIO:
    nwb_fileIO.write(content)
    nwb_fileIO.close()

nwb_file = NWBHDF5IO('output_file.nwb', 'r')
nwbfile_read = nwb_file.read()

print(nwbfile_read.electrode_groups['somename'])
