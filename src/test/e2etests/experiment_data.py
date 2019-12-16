class ExperimentData:
    animal_name = 'beans/'
    date = '20190718/'
    raw = 'raw/'
    data_set = '01_s1'
    preprocessing = 'preprocessing/'

    mda_folder = '20190718_beans_01_s1.mda/'
    mda_file = '20190718_beans_01_s1.nt1.mda'
    mda_timestamp = '20190718_beans_01_s1.timestamps.mda'

    pos_folder = '20190718_beans_01_s1.1.pos/'
    pos_file = '20190718_beans_01_s1.1.pos_online.dat'

    dio_folder = '20190718_beans_01_s1.DIO/'

    root_path = 'test_data/'
    raw_root_path = root_path + animal_name + raw
    preprocessing_root_path = root_path + animal_name + preprocessing

    mda_path = preprocessing_root_path + date + mda_folder
    pos_path = preprocessing_root_path + date + pos_folder
    metadata_path = root_path + animal_name + 'metadata.yml'

    rec_file = '20190718_beans_01_s1.rec'
    xml_file = 'fl_lab_header.xml'

    rec_path = raw_root_path + date + rec_file
    xml_path = preprocessing_root_path + date + xml_file
    xsd_path = '../data/fl_lab_header.xsd'

    path_to_extensions = '../datamigration/extension/'
    novela_namespaces = 'NovelaNeurotechnologies.namespace.yaml'
    novela_specs = 'NovelaNeurotechnologies.specs.yaml'
