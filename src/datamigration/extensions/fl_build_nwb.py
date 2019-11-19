from datetime import datetime
import numpy as np
from dateutil.tz import tzlocal
from pynwb import NWBFile
from pynwb.ecephys import ElectricalSeries

from pynwb import NWBHDF5IO

from src.datamigration.extensions.fl_probe_usage import Probe

start_time = datetime(2017, 4, 3, 11, tzinfo=tzlocal())
create_date = datetime(2017, 4, 15, 12, tzinfo=tzlocal())
nwbfile = NWBFile('demonstrate caching', 'NWB456', start_time,
                  file_create_date=create_date)

probe = Probe(name='some_probe_name', Probe_name='some_other_probe_name')

nwbfile.add_device(probe)

io = NWBHDF5IO('cache_spec_example.nwb', mode='w')
io.write(nwbfile)
io.close()


io = NWBHDF5IO('cache_spec_example.nwb', mode='r', load_namespaces=True)
nwbfile = io.read()

print(nwbfile.devices)