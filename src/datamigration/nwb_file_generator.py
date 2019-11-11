# import pynwb
#
# from src.datamigration.nwb_file_builder import NWBFileCreator
#
# if __name__ == '__main__':
#     NWBFileCreator().build()
#
#     with pynwb.NWBHDF5IO('example_file_path.nwb_builder', mode='a') as io:
#         nwbfile = io.read()
#         print(nwbfile.processing['position'].data_interfaces['Position'])
