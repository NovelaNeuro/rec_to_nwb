# plots timestamps from nwb file(e-series)
import matplotlib.pyplot as plt
from pynwb import NWBHDF5IO

from ndx_franklab_novela.header_device import HeaderDevice

nwb_file = NWBHDF5IO('rec_to_nwb/rec_to_nwb/test/beans20190718.nwb', 'r')
nwbfile_read = nwb_file.read()

timestamp = nwbfile_read.acquisition['e-series'].timestamps

plt.plot(timestamp)
plt.show()
