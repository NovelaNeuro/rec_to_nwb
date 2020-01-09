from dateutil.tz import tzlocal
from pynwb import NWBHDF5IO, NWBFile
from datetime import datetime

from pynwb.device import Device

from src.datamigration.extension.extension_builder import ExtensionsBuilder
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

probe = Probe(id=6,
                                 probe_type='probiusz typ',
                                 electrode_groups=[1, 2, 3],
                                 ntrodes=[5, 5, 5],
                                 contact_size=4.5,
                                 num_shanks=4,
                                 name='EGname',
                                 description='byly sobie swinki trzy',
                                 location='krakow',
                                 device=content.devices['trodes'],
                                 )
print(probe)
content.add_electrode_group(probe)
print(content.electrode_groups['EGname'])
a = ExtensionsBuilder('NovelaNeurotechnologies.specs.yaml', 'NovelaNeurotechnologies.namespace.yaml')
with NWBHDF5IO(path='output_file.nwb', mode='w') as nwb_fileIO:
    nwb_fileIO.write(content)
    nwb_fileIO.close()

nwb_file = NWBHDF5IO('output_file.nwb', 'r')
nwbfile_read = nwb_file.read()

print(nwbfile_read.electrode_groups['EGname'])
print(' do some')