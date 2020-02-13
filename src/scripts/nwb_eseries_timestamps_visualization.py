# plots timestamps from nwb file(e-series)
import matplotlib.pyplot as plt
from pynwb import NWBHDF5IO, load_namespaces

from src.datamigration.extension.apparatus import Apparatus
from src.datamigration.extension.edge import Edge
from src.datamigration.extension.header_device import HeaderDevice
from src.datamigration.extension.node import Node
from src.datamigration.extension.ntrode import NTrode

load_namespaces('LorenFranksDataMigration/src/datamigration/extension/NovelaNeurotechnologies.namespace.yaml')
nwb_file = NWBHDF5IO('LorenFranksDataMigration/src/test/beans20190718.nwb', 'r')
nwbfile_read = nwb_file.read()

timestamp = nwbfile_read.acquisition['e-series'].timestamps

plt.plot(timestamp)
plt.show()
