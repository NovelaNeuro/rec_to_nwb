class ExperimentData:
    animal_name = 'beans/'
    date = '20190718/'
    raw = 'raw/'
    preprocessing = 'preprocessing/'

    mda_folder = '20190718_beans_01_s1.mda/'
    mda_file = '20190718_beans_01_s1.nt1.mda'
    mda_timestamp = '20190718_beans_01_s1.timestamps.mda'

    pos_folder = '20190718_beans_01_s1.1.pos/'
    pos_file = '20190718_beans_01_s1.1.pos_online.dat'

    root_path = '../test_data/'
    raw_root_path = root_path + animal_name + raw
    preprocessing_root_path = root_path + animal_name + preprocessing

    mda_path = preprocessing_root_path + date + mda_folder
    pos_path = preprocessing_root_path + date + pos_folder
    metadata_path = preprocessing_root_path + date + 'metadata.yml'
