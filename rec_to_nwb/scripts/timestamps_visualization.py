# visualize timestamps from epoch in function of its indexes from continuoustime.dat files.
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile
import matplotlib.pyplot as plt
import numpy as np

path_epoch1 = 'GitHub/rec_to_nwb/rec_to_nwb/test/test_data/beans/preprocessing/20190718/20190718_beans_01_s1.time/20190718_beans_01_s1.continuoustime.dat'
path_epoch2 = 'GitHub/rec_to_nwb/rec_to_nwb/test/20190718_beans_02_r1.continuoustime.dat'
path_epoch3 = 'GitHub/rec_to_nwb/rec_to_nwb/test/20190718_beans_03_s2.continuoustime.dat'
path_epoch4 = 'GitHub/rec_to_nwb/rec_to_nwb/test/20190718_beans_04_r2.continuoustime.dat'
continuous_time = readTrodesExtractedDataFile(path_epoch1)
continuous_time_dict_epoch1 = {str(data[0]): float(data[1]) for data in continuous_time['data']}
print("epoch1 length: " + str(len(continuous_time_dict_epoch1)))

continuous_time = readTrodesExtractedDataFile(path_epoch2)
continuous_time_dict_epoch2 = {str(data[0]): float(data[1]) for data in continuous_time['data']}
print("epoch2 length: " + str(len(continuous_time_dict_epoch2)))

continuous_time = readTrodesExtractedDataFile(path_epoch3)
continuous_time_dict_epoch3 = {str(data[0]): float(data[1]) for data in continuous_time['data']}
print("epoch3 length: " + str(len(continuous_time_dict_epoch3)))

continuous_time = readTrodesExtractedDataFile(path_epoch4)
continuous_time_dict_epoch4 = {str(data[0]): float(data[1]) for data in continuous_time['data']}
print("epoch4 length: " + str(len(continuous_time_dict_epoch4)))

y1 = np.array(list(continuous_time_dict_epoch1.values())).astype(float)
x1 = np.array(list(continuous_time_dict_epoch1.keys())).astype(float)

y2 = np.array(list(continuous_time_dict_epoch2.values())).astype(float)
x2 = np.array(list(continuous_time_dict_epoch2.keys())).astype(float)

y3 = np.array(list(continuous_time_dict_epoch3.values())).astype(float)
x3 = np.array(list(continuous_time_dict_epoch3.keys())).astype(float)

y4 = np.array(list(continuous_time_dict_epoch4.values())).astype(float)
x4 = np.array(list(continuous_time_dict_epoch4.keys())).astype(float)

plt.plot(x1, y1, '-g', x2, y2, '--c', x3, y3, '-.k', x4, y4, ':r')
plt.show()
