import logging
from rec_to_binaries import extract_trodes_rec_file

logging.basicConfig(level='INFO', format='%(asctime)s %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

data_dir = 'test_data/'
animal = 'lotus'

extract_trodes_rec_file(data_dir, animal, parallel_instances=4)