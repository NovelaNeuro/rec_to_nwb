import loren_frank_data_processing as lfdp
from loren_frank_data_processing import Animal
import pandas as pd
import numpy as np
import yaml
import scipy.io as si 

def generate_day_yaml(animal,sess_id):
    # animal = 'montague'
    # sess_id = 14
    #ffdir = '/Users/asilva/Documents/mount/stelmo/anna/' + animal + '/filterframework/';
    base_dir = '/stelmo/anna/' + animal
    ffdir = base_dir + '/filterframework/';

    template_yaml = '/home/asilva/src/mat_to_nwb/despereaux20191122.yml';
    pad_sess = "{:02d}".format(sess_id)

    # trials = si.loadmat(ffdir + animal + 'trials' + pad_sess + '.mat')
    task = si.loadmat(ffdir + animal + 'task' + pad_sess + '.mat')
    # tetinfo = si.loadmat(ffdir + animal + 'tetinfo.mat')

    # pull off the date that corresponds to the session id 
    date = str(int(task['task'][0,sess_id-1][0,1]['date']))


    rat_name = animal
    raw_directory = ffdir
    animalinfo  = {rat_name: Animal(directory=raw_directory, short_name=rat_name)}
    tetinfo = lfdp.tetrodes.make_tetrode_dataframe(animalinfo)
    taskinfo=lfdp.make_epochs_dataframe(animalinfo)
    taskinfo = taskinfo.reset_index()

    # get the relevant day task info
    day_task = taskinfo[taskinfo['day'] == sess_id]
    day_task['letter'] = day_task['type'].apply(lambda x: x[0])
    day_task['epoch_pad'] = day_task['epoch'].apply(lambda x: "{:02d}".format(x))

    #Load YAML file 
    a_yaml_file = open(template_yaml)
    yam_temp = yaml.load(a_yaml_file, Loader=yaml.FullLoader)

    # figure out which number run and sleep each epoch is 
    sleep_num = 0
    run_num = 0
    labels = []
    for l in day_task['letter']:
        if(l=='s'):
            sleep_num += 1
            labels.append((sleep_num))
        else:
            run_num += 1
            labels.append((run_num))

    day_task['type_num'] = labels

    # put on the associated file and the the video file 
    day_task['asc_file'] = day_task[['letter','epoch_pad','type_num']].apply(lambda x: base_dir + '/raw/'+ date 
                                   +'/' + date + '_' + animal + '_' + x[1] + '_' + x[0] 
                                   + str(x[2]) + '.stateScriptLog',axis=1)

    day_task['vid_file'] = day_task[['letter','epoch_pad','type_num']].apply(lambda x: date + '_' + animal + '_' + x[1]
                                   + '_' + x[0] + str(x[2]) + '.1.h264',axis=1)

    # put in the camera value for each. First we have to see what camera corresponds to run and sleep
    cams = yam_temp['cameras']
    if('sleep' in cams[0]['camera_name']):
        sleep_cam_id = 0
        run_cam_id = 1
    else: 
        sleep_cam_id = 1
        run_cam_id = 0

    day_task['camera'] = day_task['letter'].apply(lambda x: sleep_cam_id if x=='s' else run_cam_id)

    # define the statescript path 
    ss_path = '/stelmo/anna/' + animal + '/raw/' + date + '/';


    # write over the session id
    yam_temp['session_id'] = animal + '_' + pad_sess

    # write over the subject id
    yam_temp['subject']['subject_id'] = animal

    # get the associated files for each task and overwrite 
    assoc_files = []
    for index, row in day_task.iterrows():
        cur_dict = {}
        cur_dict['name'] = 'statescript_' + row['letter'] + str(row['type_num'])
        cur_dict['description'] = 'Statescript log ' + row['letter'] + str(row['type_num'])
        cur_dict['path'] = row['asc_file']
        cur_dict['task_epochs'] = [row['epoch']]
        assoc_files.append(cur_dict)

    # overwrite the template
    yam_temp['associated_files'] = assoc_files

    # get the associated video files and overwrite 
    assoc_vid_files = []
    for index, row in day_task.iterrows():
        cur_dict = {}
        cur_dict['name'] = row['vid_file']
        cur_dict['camera_id'] = row['camera']
        cur_dict['task_epoch'] = row['epoch']
        assoc_vid_files.append(cur_dict)

    yam_temp['associated_video_files'] = assoc_vid_files

    # get the behavioral events and overwrite 
    # 9 -- hardcoded based on the format of task.mat files 
    behave_events = (task['task'][0,sess_id-1][0,1][0,0][9][0,0][0])
    behave_evt_map = []
    for i in range(0,behave_events.shape[0]):
        cur_dict = {}
        cur_dict['description'] = str(behave_events[i,1][0])
        cur_dict['name']  = str(behave_events[i,0][0])
        behave_evt_map.append(cur_dict)

    yam_temp['behavioral_events'] = behave_evt_map

    # write over the electrode groups 
    tmp_elec_group = yam_temp['electrode_groups'][0]

    # first need to pull out the relevant tetrode information 
    tetinfo = tetinfo.reset_index()
    tet_day = tetinfo[(tetinfo['day'] == sess_id) & (tetinfo['epoch']== 1)]
    all_elec_groups = []
    for index, row in tet_day.iterrows():
        cur_dict = tmp_elec_group.copy()
        cur_dict['id'] = row['tetrode_number'] - 1
        # make nan --> ''
        if(isinstance(row['area'],float)):
            if(np.isnan(row['area'])):
                row['area'] = ''
        cur_dict['location'] = row['area']
        cur_dict['targeted_location'] = 'CA1'
        all_elec_groups.append(cur_dict)

    yam_temp['electrode_groups'] = all_elec_groups 

   
    for i in range(0,len(yam_temp['ntrode_electrode_group_channel_map'])):
        row = tet_day.iloc[i,:]
        yam_temp['ntrode_electrode_group_channel_map'][i]['ntrode_id'] = int(row['tetrode_number'])
        yam_temp['ntrode_electrode_group_channel_map'][i]['electrode_group_id'] = int(row['tetrode_number'] - 1)
        deadchans = row['deadchans']
        if(isinstance(deadchans,int)):
            deadchans = [deadchans]
        elif isinstance(deadchans, float):
            if np.isnan(deadchans):
                deadchans = []
            else:
                deadchans = [deadchans]
        else:
            deadchans = deadchans.tolist()
        yam_temp['ntrode_electrode_group_channel_map'][i]['bad_channels'] = deadchans 


    # overwrite the tasks section 

    # put in the sleep epochs first 
    yam_temp['tasks'][0]['task_epochs'] = day_task['epoch'][day_task['letter'] == 's'].tolist()

    # now the run epochs 
    yam_temp['tasks'][1]['task_epochs'] = day_task['epoch'][day_task['letter'] == 'r'].tolist()


    #write out the yaml 
    out_file = '/home/asilva/src/mat_to_nwb/yaml_files/' + animal + date + '.yaml'
    stream = open(out_file, 'w')
    yaml.dump(yam_temp, stream)    # Write a YAML representation of data to 'document.yaml'.

    