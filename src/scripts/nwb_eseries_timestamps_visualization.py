# plots timestamps from nwb file(e-series)
import matplotlib.pyplot as plt
from pynwb import NWBHDF5IO

from ndx_franklab_novela.apparatus import Apparatus
from ndx_franklab_novela.edge import Edge
from ndx_franklab_novela.header_device import HeaderDevice
from ndx_franklab_novela.node import Node
from ndx_franklab_novela.ntrode import NTrode

nwb_file = NWBHDF5IO('LorenFranksDataMigration/src/test/beans20190718.nwb', 'r')
nwbfile_read = nwb_file.read()

timestamp = nwbfile_read.acquisition['e-series'].timestamps

plt.plot(timestamp)
plt.show()
