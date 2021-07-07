import os
import logging
import sys
from rec_to_nwb.processing.builder.nwb_file_builder import NWBFileBuilder
from rec_to_binaries import extract_trodes_rec_file
from rec_to_nwb.processing.builder.raw_to_nwb_builder import RawToNWBBuilder
from rec_to_nwb.processing.metadata.metadata_manager import MetadataManager
import scipy.io as si 

def generate_day_nwb(animal,sess_id):
    # get the date that corresponds to animal and sess_id
    base_dir = '/stelmo/anna/' + animal
    ffdir = base_dir + '/filterframework/';
    pad_sess = "{:02d}".format(sess_id)    
    task = si.loadmat(ffdir + animal + 'task' + pad_sess + '.mat')
    # pull off the date that corresponds to the session id 
    date = str(int(task['task'][0,sess_id-1][0,1]['date']))
    # set the animal name and the date or list of dates to process
    dates = [date]
    # note that code currently only takes one date at a time;
    # build a loop through date strings to create multiiple nwb files at once

    # path to dir containing device and animal/date .yml files
    # for example, '/home/<yourusername>/Src/franklabnwb/yaml'
    yaml_path = '/home/asilva/src/mat_to_nwb/yaml_files/' + animal
    # metadata filename for an animal and date. This is a file that you generate as the user.
    # for example,  '<ratname><date>_metadata.yml'
    animal_metadata_file = animal + date + '.yaml' #bad_channels in yaml will be left out of the .nwb filie
    # metadata filename for a recording device type;
    # typically these are common lab files that you shouldn't need to personalize

    probe1_metadata_file = 'tetrode_12.5.yml'


    #probe1_metadata_file = '128c-4s8mm6cm-20um-40um-sl.yml'
    #probe2_metadata_file = 'tetrode_12.5.yml'

    # Specify the paths for the data, the output nwb file, and the video files
    # example raw data INPUT path: '/stelmo/<yourusername>/'
    data_path = '/stelmo/anna/'
    # the nwb file OUTPUT path should be '/stelmo/nwb/raw'
    # FOR BATCH CHANGE TO ANNA FOLDER
    output_path='/stelmo/anna/nwb/raw/'
    #  video OUTPUT path should be '/stelmo/nwb/video'
    # just copies over the raw video files into this dir
    video_path='/stelmo/anna/nwb/video'
    # note that a rec_to_nwb.log file will also be saved to the directory from which your are running this notebook

    # Specify any optional trodes export flags
    # uses rec_to_binaries repo, which uses SpikeGadgets/Trodes export functions
    # keep things as raw as possible though - unlike old preprocessing pipeline, 
    # we aren't doing any filtering or interpolation yet
    trodes_rec_export_args = ('-reconfig', '/stelmo/anna/' + animal +'/raw/' + date + '/' + date + '.trodesconf')       

    # specify the locations of the metadata files for the animal and the probe(s). 
    # Note that specifying all possible probes is fine
    animal_metadata = os.path.join(yaml_path, animal_metadata_file )

    probe_metadata = [os.path.join(yaml_path, probe1_metadata_file)] 
    # probe_metadata = [os.path.join(yaml_path, probe1_metadata_file), 
    #                   os.path.join(yaml_path, probe2_metadata_file)]

    # Specify whether preprocessing data should be reextracted (True) or skipped if it already exists (False)
    overwrite=True
    # note that extraction will write to the directory: data_path+'preprocessing/' and
    # you may have data you previously preprocessed in that dir, created with alternate export args
    # that you neither want to skip nor overwrite if you're using them for filterframework
    metadata = MetadataManager(animal_metadata, probe_metadata)
    # build the run enviornment 
    animal_name = animal	
    builder = RawToNWBBuilder(animal_name=animal_name,
                          data_path=data_path,
                          dates=dates,
                          nwb_metadata=metadata,
                          overwrite=overwrite,
                          output_path=output_path,
                          video_path=video_path,
                          trodes_rec_export_args = trodes_rec_export_args)
    # run the processing 
    content = builder.build_nwb()
