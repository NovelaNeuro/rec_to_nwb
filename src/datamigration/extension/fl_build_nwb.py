from datetime import datetime

from dateutil.tz import tzlocal
from pynwb import NWBFile
from pynwb import NWBHDF5IO

from src.fl_probe import Probe

start_time = datetime(2017, 4, 3, 11, tzinfo=tzlocal())
create_date = datetime(2017, 4, 15, 12, tzinfo=tzlocal())
nwbfile = NWBFile('demonstrate caching', 'NWB456', start_time,
                  file_create_date=create_date)

probe = Probe(name='some_probe_name', Probe_name='some_other_probe_name')

nwbfile.add_device(probe)
nwbfile.create_electrode_group(name='some novela electrode group', description='some desc', location='xyzlocation', device=probe)
nwbfile.create_electrode_group(name='some novela electrode group2', description='some desc1', location='xyzlocation33', device=probe)
nwbfile.create_electrode_group(name='some novela electrode group3', description='some desc2', location='xyzlocation44', device=probe)

io = NWBHDF5IO('cache_spec_example.nwb', mode='w')
io.write(nwbfile)
io.close()


io = NWBHDF5IO('cache_spec_example.nwb', mode='r', load_namespaces=True)
nwbfile = io.read()

print(nwbfile.electrode_groups)