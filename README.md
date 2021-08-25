# rec_to_nwb
# About
rec_to_nwb is a python conda package for converting SpikeGadgets rec files to NWB files.<br>
It converts experiment data from `/raw` or `/preprocessing` folder to `.nwb` file. It utilizes rec_to_binaries package for preprocessing phase.<br>
<https://github.com/LorenFrankLab/rec_to_binaries><br>

# Instructions:
Currently we suggest following the instructions to install https://github.com/LorenFrankLab/franklabnwb, as that includes additional files that are helpful, but you can install this using the instructions below.

## For developers
1. Install Spike Gadgets <br>
   <https://bitbucket.org/mkarlsso/trodes/downloads/>
2. Add SpikeGadgets to path. <br>
   If Spike Gadgets is in default location:
   ```bash
   export PATH="$HOME/SpikeGadgets/:$PATH"
   ```
3. Install anaconda or miniconda if you haven't already.

4. clone repository
   ```bash
   git clone https://github.com/LorenFrankLab/rec_to_nwb.git

   cd rec_to_nwb
   ```
5. Create conda environment.
   ```bash
   conda env create -f environment.yml
   ```
6. Install rec_to_nwb
   ```bash
   cd ..
   python setup.py install
   ```
7. jupyter notebook installation
   ```bash
   pip install jupyter notebook
   ```
8. Documentation can be viewed at <br>
    <https://novelaneuro.github.io/rec_to_nwb-docs/>

# How to use it
1. Download example notebook file from <br>
   <https://anaconda.org/NovelaKRK/nwb_generation/notebook>
2. In terminal navigate to notebook file location
   ```bash
   rec_to_nwb/rec_to_nwb/notebooks
   ```
3. Run jupyter notebook
   ```bash
   jupyter notebook nwb_generation.ipynb
   ```
4. Metadata.yml description:

Important note: right now the code assumes that the electrode groups listed below (each of which corresponds to one or more NTrode in the file) are in ascending order by NTrode number. If this is not the case the data could be scrambled.  Thus, the first listed electrode group should correspond to, for example, NTrode 1 (or perhaps NTrodes 1-4) while the second would correspond to NTrode 2 (or 5-8), etc.  


   ```yaml
    # general information about the experiment
    experimenter_name: Alison Comrie
    lab: Loren Frank
    institution: University of California, San Francisco
    experiment_description: Reinforcement learning
    session_description: Reinforcement leaarning
    session_id: beans_01
    subject:
      description: Long Evans Rat
      genotype: Wild Type
      sex: Male
      species: Rat
      subject_id: Beans
      weight: Unknown
   #Units of analog and behavioral_events
   units:
      analog: 'unspecified'
      behavioral_events: 'unspecified'  
   #data_acq_device used in experiment   
   data_acq_device:
      - name: acq_0
        system: sample_system
        amplifier: sample_amplifier
        adc_circuit: sample_adc_circuit
      - name: acq_1
        system: sample_system_2
   #CameraDevice that were used in experiment    
    cameras:
      - id: 0
        meters_per_pixel: 0.02
      - id: 1
        meters_per_pixel: 0.03
      - id: 2
        meters_per_pixel: 0.05  
    #Tasks represent epochs in experiment. Contains task_name, task_description, camera_id that were used in this task and task_epochs that this task correspond to. Stored in behavioral section in output nwb file.
    tasks:
      - task_name:          Sleep,
        task_description:   The animal sleeps in a small empty box.
        camera_id:
          - 0
        task_epochs:
          - 1
          - 3
          - 5
      - task_name:            Stem+Leaf,
        task_description:     Spatial Bandit,
        camera_id:
          - 1
        task_epochs:
          - 2
          - 4
    # Associated files which describe content of files stored inside nwb as text.
       associated_files:
      -  name: example_name1
         description: exmaple description 1
         path: C:/Users/sampleuser/PycharmProjects/rec_to_nwb/test/processing/res/test_text_files/test1_file
         task_epochs: [1, 2]
      -  name: example_name2
         description: exmaple description 2
         path: C:/Users/sampleuser/PycharmProjects/rec_to_nwb/test/processing/res/test_text_files/test2_file
         task_epochs: [3, 4]
    # Associated video files describe .h264 files stored as ImageSeries in nwb.
       associated_video_files:
      - name: 20190718_beans_01_s1.1.h264
        camera_id : 0
    # Times period multiplier is used in pos/mda invalid/valid times, to multiply the period when detecting gaps,
        to avoid creating invalid times in case of only small deviations. (optional parameter, default 1.5)
       times_period_multiplier: 1.5      
    # Din/Dout events which filter out files from DIO data in data directory. Each name has to be unique. Stored in behavioral_events section in output nwb file.
    behavioral_events:
      - name: Poke2
        description: Din2
    # Device name. Stored in output nwb file.
    device:
      name:
        - Trodes
    # Electrode Groups list used in experiment. Each Id has to be unique, device_type has to refer to existing device_type in probe.yml. Target_x,y,z fields describe the specified location where this group should be. Possible value of units: 'um' or 'mm'
    electrode_groups:
      - id: 0
        location: mPFC
        device_type: 128c-4s8mm6cm-20um-40um-sl
        description: 'Probe 1'
        targeted_location: 'Sample predicted location'
        targeted_x: 0.0
        targeted_y: 0.0
        targeted_z: 0.0
        units: 'um'
      - id: 1
        location: mPFC
        device_type: 128c-4s8mm6cm-20um-40um-sl
        description: 'Probe 2'
        targeted_location: 'Sample predicted location'
        targeted_x: 0.0
        targeted_y: 0.0
        targeted_z: 0.0
        units: 'um'
    # Ntrodes list which refer 1:1 to <SpikeNTrode> elements from xml header existing in rec binary file.
    # ntrode_id has to match to SpikeNTrode id, electrode_group_id refers to electrode group,
    # bad_channels is a list of broken channels in the map, where map corresponds to the electrode channels
      - ntrode_id: 1
        electrode_group_id: 0
        bad_channels: [0,2]
        map:  
          0: 0
          1: 1
          2: 2
          3: 3
      - ntrode_id: 2
        electrode_group_id: 0
        bad_channels: [0,2]
        map:
          0: 4
          1: 5
          2: 6
          3: 7
    ```
5. Probe.yml description:
   ```yaml
    probe_type: tetrode_12.5 # Type of the probe that refers to device_type in electrode_group in metadata.yml
    units: 'um' # possible value for unit is um or mm
    probe_description: 'four wire electrode'
    num_shanks: 1 # Number of shanks (sets of electrodes) in this probe type
    contact_side_numbering: true
    contact_size: 12.5
    shanks:
      - shank_id: 0 # Shank_id has to be unique
        electrodes: # List of electrodes that is used to initialize the electrode_table in output nwb file
          - id: 0 # Electrode id has to be unique
            rel_x: 0.0
            rel_y: 0.0
            rel_z: 0.0
          - id: 1
            rel_x: 0.0
            rel_y: 0.0
            rel_z: 0.0
   ```
6. Set up paths to metadata and probe `yaml` files, which corresponds to the experiment you are going to process.
   ```bash
   metadata = MetadataManager(
        '../test/processing/res/metadata.yml',
        ['../test/processing/res/probe1.yml',
        '../test/processing/res/probe2.yml',
        '../test/processing/res/probe3.yml']  
   )
   ```
7. Input files `metadata.yml` as well as `probe[1-N].yml` are validated against rec files headers.

8. We provide two class to generate the NWB file. <br>
* `RawToNWBBuilder` - To generate NWB file from raw data. <br>
* `NWBFileBuilder` - To generate NWB file from preprocessed data. <br>

##### Raw data
Initialize RawToNWBBuilder, which requires `animal_name`, `data_path` and `dates` which exist in your experiment folder. Next build the NWB using `build_nwb()`. <br>
If you don't want mda or pos invalid/valid times in your nwb, set accordingly flag to false in 'build_nwb' method.

   ```bash
   builder = RawToNWBBuilder(
             animal_name='beans',
             data_path='../test/test_data/',
             dates=['20190718'],
             nwb_metadata=metadata,
             output_path='/out/nwb'
              )
   builder.build_nwb()
   ```
   raw_to_nwb_builder arguments

      **data_path** = `string` path to the parent folder of animal_name <br>

      **animal_name** = `string` name of the folder that contain few dates-folders <br>

      **dates** = `list of strings` names of folders that contain experiment data <br>

      **nwb_metadata** = `MetadataManager` object with metadata.yml and probes.yml <br>

      **output_path** = `string` path specifying location and name of result file (dafault 'output.nwb') <br>

      **video_path** = `string` path specifying location of video files .h264 where those are copied <b4>

      **extract_analog** = `boolean` flag specifying if analog data should be extracted from raw (default True) <br>

      **extract_spikes** = `boolean` flag specifying if spikes data should be extracted from raw (default False) <br>

      **extract_lfps** = `boolean` flag specifying if lfp data should be extracted from raw (default False) <br>

      **extract_dio** = `boolean` flag specifying if dio data should be extracted from raw (default True) <br>

      **extract_mda** = `boolean` flag specifying if mda data should be extracted from raw (default True) <br>

      **parallel_instances** = `int` number of threads, optimal value highly depends on hardware (default 4) <br>

      **overwrite** = `boolean`  If true, will overwrite existing files. (default True) <br>

      **trodes_rec_export_args** = `tuple of strings` path to rec header file which overrides all headers existing in rec binary files e.g `_DEFAULT_TRODES_REC_EXPORT_ARGS = ('-reconfig', str(path) + '/test/processing/res/reconfig_header.xml')` <br>  

   build_nwb arguments:

     **process_mda_valid_time** = 'boolean' True if the mda valid times should be build and append to nwb.
                Need the mda data inside the nwb. (default True) <br>

     **process_mda_invalid_time** = 'boolean' True if the mda invalid times should be build and append to nwb.
                Need the mda data inside the nwb. (default True) <br>

     **process_pos_valid_time** = 'boolean' True if the pos valid times should be build and append to nwb.
                Need the pos data inside the nwb. (default True) <br>

     **process_pos_invalid_time** = 'boolean' True if the pos invalid times should be build and append to nwb.
                Need the pos data inside the nwb. (default True) <br>

##### Preprocessed data
If you have already preprocessed data or RawToNwb process crashed during building file you can initialize NWBFileBuilder, which requires `data_path`, `animal_name`, `date`, `nwb_metadata`.  
Next build the NWB using `build()` and write it to file by `write(content)` method.
After that, you can add mda or pos invalid/valid data to your NWB, using 'build_and_append_to_nwb' method.

   ```bash
   builder = NWBFileBuilder(
            data_path='../data/',
            animal_name='beans',
            date='20190718',
            nwb_metadata=metadata,
            process_dio=True,
            process_mda=True,
            process_analog=True
        )
   content = builder.build()
   builder.write(content)
   ```
   NWBFileBuilder arguments

     **data_path** = `string` path to directory containing all experiments data <br>

     **animal_name** = `string` directory name which represents animal subject of experiment <br>

     **date** = `string` date of experiment <br>

     **nwb_metadata** = `MetadataManager` object contains metadata about experiment <br>

     **process_dio** = `boolean` flag if dio data should be processed <br>

     **process_mda** = `boolean` flag if mda data should be processed <br>

     **process_analog** = `boolean` flag if analog data should be processed <br>

     **video_path** = `string` path specifying location of video files .h264 where those are copied <b4>

     **output_file** = `string` path and name specifying where .nwb file gonna be written <br>

   build_and_append_to_nwb arguments:

     **process_mda_valid_time** = 'boolean' True if the mda valid times should be build and append to nwb.
                Need the mda data inside the nwb. (default True) <br>

     **process_mda_invalid_time** = 'boolean' True if the mda invalid times should be build and append to nwb.
                Need the mda data inside the nwb. (default True) <br>

     **process_pos_valid_time** = 'boolean' True if the pos valid times should be build and append to nwb.
                Need the pos data inside the nwb. (default True) <br>

     **process_pos_invalid_time** = 'boolean' True if the pos invalid times should be build and append to nwb.
                Need the pos data inside the nwb. (default True) <br>

9. Make sure that the data structure in given directory (in that case `test_data`) looks similar to following example:
   ```bash
    --test_data
      |
      `-- beans
          |   |
          |   `-- raw
          |       |
          |       `-- 20190718
          |           |-- 20190718_beans_01_s1.1.h264
          |           |-- 20190718_beans_01_s1.1.trackgeometry
          |           |-- 20190718_beans_01_s1.1.videoPositionTracking
          |           |-- 20190718_beans_01_s1.1.videoTimeStamps
          |           |-- 20190718_beans_01_s1.1.videoTimeStamps.cameraHWSync
          |           |-- 20190718_beans_01_s1.rec
          |           `-- 20190718_beans_01_s1.stateScriptLog
          `-- README.md

   ```

10. Double check if there is enough disc space on your Laptop/PC.

11. Run processing (generation may take from mins to even hours and it depends on the size of experiment datasets).

12. `rec_to_nwb.log` contains useful information about processing phases as well as all of the exceptions and errors.

13. Example structure of preprocessed experiment data
   ```bash
   |-- beans
   |   |-- preprocessing
   |   |   |
   |   |   |-- 20190718
   |   |       |-- 20190718_beans_01_s1.1.pos
   |   |       |   |-- 20190718_beans_01_s1.1.pos_cameraHWFrameCount.dat
   |   |       |   |-- 20190718_beans_01_s1.1.pos_online.dat
   |   |       |   |-- 20190718_beans_01_s1.1.pos_timestamps.dat
   |   |       |-- 20190718_beans_01_s1.analog
   |   |       |   |-- 20190718_beans_01_s1.analog_AccelX.dat
   |   |       |   |-- 20190718_beans_01_s1.analog_AccelY.dat
   |   |       |   |-- 20190718_beans_01_s1.analog_AccelZ.dat
   |   |       |   |-- 20190718_beans_01_s1.analog_GyroX.dat
   |   |       |   |-- 20190718_beans_01_s1.analog_GyroY.dat
   |   |       |   |-- 20190718_beans_01_s1.analog_GyroZ.dat
   |   |       |   |-- 20190718_beans_01_s1.analog_MagX.dat
   |   |       |   |-- 20190718_beans_01_s1.analog_MagY.dat
   |   |       |   |-- 20190718_beans_01_s1.analog_MagZ.dat
   |   |       |   |-- 20190718_beans_01_s1.exportanalog.log
   |   |       |   |-- 20190718_beans_01_s1.timestamps.dat
   |   |       |-- 20190718_beans_01_s1.DIO
   |   |       |   |-- 20190718_beans_01_s1.dio_Din10.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din11.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din12.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din13.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din14.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din15.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din16.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din17.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din18.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din19.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din1.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din20.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din21.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din22.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din23.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din24.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din25.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din26.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din27.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din28.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din29.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din2.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din30.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din31.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din32.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din3.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din4.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din5.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din6.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din7.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din8.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Din9.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout10.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout11.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout12.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout13.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout14.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout15.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout16.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout17.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout18.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout19.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout1.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout20.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout21.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout22.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout23.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout24.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout25.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout26.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout27.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout28.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout29.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout2.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout30.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout31.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout32.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout3.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout4.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout5.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout6.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout7.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout8.dat
   |   |       |   |-- 20190718_beans_01_s1.dio_Dout9.dat
   |   |       |   |-- 20190718_beans_01_s1.exportdio.log
   |   |       |-- 20190718_beans_01_s1.LFP
   |   |       |   |-- 20190718_beans_01_s1.exportLFP.log
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt10ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt11ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt12ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt13ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt14ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt15ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt16ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt17ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt18ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt19ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt1ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt20ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt21ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt22ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt23ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt24ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt25ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt26ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt27ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt28ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt29ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt2ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt30ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt31ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt32ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt3ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt4ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt5ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt6ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt7ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt8ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.LFP_nt9ch1.dat
   |   |       |   |-- 20190718_beans_01_s1.timestamps.dat
   |   |       |-- 20190718_beans_01_s1.mda
   |   |       |   |-- 20190718_beans_01_s1.exportmda.log
   |   |       |   |-- 20190718_beans_01_s1.nt10.mda
   |   |       |   |-- 20190718_beans_01_s1.nt11.mda
   |   |       |   |-- 20190718_beans_01_s1.nt12.mda
   |   |       |   |-- 20190718_beans_01_s1.nt13.mda
   |   |       |   |-- 20190718_beans_01_s1.nt14.mda
   |   |       |   |-- 20190718_beans_01_s1.nt15.mda
   |   |       |   |-- 20190718_beans_01_s1.nt16.mda
   |   |       |   |-- 20190718_beans_01_s1.nt17.mda
   |   |       |   |-- 20190718_beans_01_s1.nt18.mda
   |   |       |   |-- 20190718_beans_01_s1.nt19.mda
   |   |       |   |-- 20190718_beans_01_s1.nt1.mda
   |   |       |   |-- 20190718_beans_01_s1.nt20.mda
   |   |       |   |-- 20190718_beans_01_s1.nt21.mda
   |   |       |   |-- 20190718_beans_01_s1.nt22.mda
   |   |       |   |-- 20190718_beans_01_s1.nt23.mda
   |   |       |   |-- 20190718_beans_01_s1.nt24.mda
   |   |       |   |-- 20190718_beans_01_s1.nt25.mda
   |   |       |   |-- 20190718_beans_01_s1.nt26.mda
   |   |       |   |-- 20190718_beans_01_s1.nt27.mda
   |   |       |   |-- 20190718_beans_01_s1.nt28.mda
   |   |       |   |-- 20190718_beans_01_s1.nt29.mda
   |   |       |   |-- 20190718_beans_01_s1.nt2.mda
   |   |       |   |-- 20190718_beans_01_s1.nt30.mda
   |   |       |   |-- 20190718_beans_01_s1.nt31.mda
   |   |       |   |-- 20190718_beans_01_s1.nt32.mda
   |   |       |   |-- 20190718_beans_01_s1.nt3.mda
   |   |       |   |-- 20190718_beans_01_s1.nt4.mda
   |   |       |   |-- 20190718_beans_01_s1.nt5.mda
   |   |       |   |-- 20190718_beans_01_s1.nt6.mda
   |   |       |   |-- 20190718_beans_01_s1.nt7.mda
   |   |       |   |-- 20190718_beans_01_s1.nt8.mda
   |   |       |   |-- 20190718_beans_01_s1.nt9.mda
   |   |       |   |-- 20190718_beans_01_s1.timestamps.mda
   |   |       |-- 20190718_beans_01_s1.mountain
   |   |       |-- 20190718_beans_01_s1.spikes
   |   |       |   |-- 20190718_beans_01_s1.exportspikes.log
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt10.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt11.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt12.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt13.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt14.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt15.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt16.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt17.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt18.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt19.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt1.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt20.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt21.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt22.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt23.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt24.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt25.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt26.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt27.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt28.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt29.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt2.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt30.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt31.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt32.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt3.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt4.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt5.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt6.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt7.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt8.dat
   |   |       |   |-- 20190718_beans_01_s1.spikes_nt9.dat
   |   |       |-- 20190718_beans_01_s1.time
   |   |           |-- 20190718_beans_01_s1.continuoustime.dat
   |   |           |-- 20190718_beans_01_s1.exporttime.log
   |   |           |-- 20190718_beans_01_s1.time.dat
   |   |-- raw
   |       |-- 20190718
   |           |-- 20190718_beans_01_s1.1.h264
   |           |-- 20190718_beans_01_s1.1.trackgeometry
   |           |-- 20190718_beans_01_s1.1.videoPositionTracking
   |           |-- 20190718_beans_01_s1.1.videoTimeStamps
   |           |-- 20190718_beans_01_s1.1.videoTimeStamps.cameraHWSync
   |           |-- 20190718_beans_01_s1.rec
   |           |-- 20190718_beans_01_s1.stateScriptLog
   |-- README.md
   ```
When processing completes, a nwb file is created in the output_path directory
