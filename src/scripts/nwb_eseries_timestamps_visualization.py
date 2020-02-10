# plots timestamps from nwb file(e-series)
import matplotlib.pyplot as plt
from pynwb import NWBHDF5IO, load_namespaces

load_namespaces('LorenFranksDataMigration/src/datamigration/extension/NovelaNeurotechnologies.namespace.yaml')
nwb_file = NWBHDF5IO('LorenFranksDataMigration/src/test/e2etests/output.nwb', 'r')
nwbfile_read = nwb_file.read()

timestamp = nwbfile_read.acquisition['e-series'].timestamps

plt.plot(timestamp)
plt.show()
