import logging.config
import os

import numpy as np
from mountainlab_pytools.mdaio import writemda

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=path + '/../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


for i in range(1, 4):
    data = [[i, i, i],
            [i, i, i],
            [i, i, i]]
    arr = np.array(data, 'int16')
    name = 'res/20190718_beans_01_s1.nt' + str(i) + '.mda'
    writemda(X=arr, fname=name, dtype='int16')
