import numpy as np
from mountainlab_pytools.mdaio import writemda

for i in range(1, 4):
    data = [[i, i, i],
            [i, i, i],
            [i, i, i]]
    arr = np.array(data, 'int16')
    name = '20190718_beans_01_s1.nt' + str(i) + '.mda'
    writemda(X=arr, fname=name, dtype='int16')
