# fldatamigration
# About
fldatamigration is a python package for converting SpikeGadgets rec files to NWB files.<br>
It converts experiment data from `/raw` folder to `.nwb` file. It utilizes rec_to_binaries package for preprocessing phase.<br>
<https://github.com/LorenFrankLab/rec_to_binaries><br>

# Prerequisites
## For users
1. Install Spike Gadgets <br>
   <https://bitbucket.org/mkarlsso/trodes/downloads/>
2. Add SpikeGadgets to path. <br>
   If Spike Gadgets is in default location: <br>
   ```bash
   export PATH="$HOME/SpikeGadgets/:$PATH"
   ```
3. Download miniconda from <br>
   <https://docs.conda.io/en/latest/miniconda.html> <br>
4. Download `fldatamigration.yml` from <br>
   <https://anaconda.org/NovelaKRK/fldatamigration/files>
5. Build fldatamigration environment:
   ```bash
   conda env create -f fldatamigration.yml
   ```
6. Install Jupyter notebook
   ```bash
   pip install jupyter notebook
   ```

## For developers
1. Install Spike Gadgets <br>
   <https://bitbucket.org/mkarlsso/trodes/downloads/>
2. Add SpikeGadgets to path. <br>
   If Spike Gadgets is in default location:
   ```bash
   export PATH="$HOME/SpikeGadgets/:$PATH"
   ```
3. Download miniconda from<br>
   <https://docs.conda.io/en/latest/miniconda.html><br>
4. clone repository
   ```bash
   git clone https://github.com/NovelaNeuro/fldatamigration.git

   cd fldatamigration/fl
   ```
5. Create conda environment.
   ```bash
   conda env create -f environment.yml
   ```
6. jupyter notebook installation
   ```bash
   pip install jupyter notebook
   ```
7. Documentation can be viewed at <br>
    <https://novelaneuro.github.io/fldatamigration-docs/>

# How to use it
1. Download example notebook file from <br>
   <https://anaconda.org/NovelaKRK/nwb_generation/notebook>
2. In terminal navigate to notebook file location
3. Run jupyter notebook
   ```bash
   jupyter notebook
   ```
4. Metadata.yml description:
   ```
    # general information about the experiment 
    experimenter name: Alison Comrie
    lab: Loren Frank
    institution: University of California, San Francisco
    experiment description: Reinforcement learning
    session description: Reinforcement leaarning
    session_id: beans_01
    subject:
      description: Long Evans Rat
      genotype: Wild Type
      sex: Male
      species: Rat
      subject id: Beans
      weight: Unknown
    #Tasks represent epochs in experiment. Contain task_name and task_description in the list. Stored in behavioral section in output nwb file.
    tasks:   [
      {
        task_name: Sleep,
        task_description: The animal sleeps in a small empty box.
      },
      {
        task_name: Stem+Leaf,
        task_description: Spatial Bandit,
      }
      ]
    # Din/Dout events which filter out files from DIO data in data directory. Each name has to be unique. Stored in behavioral_events section in output nwb file.
    behavioral_events: 
      - name: Din1
      - name: Din2
        description: Poke2
    # Device name. Stored in output nwb file.
    device: 
      name:
        - Trodes
    # Probes/Electrode Groups list used in experiment. Each Id has to be unique, device_type has to refer to existing device_type in probe.yml
    electrode groups:
      - id: 0
        location: mPFC
        device_type: 128c-4s8mm6cm-20um-40um-sl 
        description: 'Probe 1'
      - id: 1
        location: mPFC
        device_type: 128c-4s8mm6cm-20um-40um-sl
        description: 'Probe 2'
    # Ntrodes list which refer 1:1 to <SpikeNTrode> elements from xml header existing in rec binary file.
    # ntrode_id has to match to SpikeNTrode id, probe_id refers to electrode group,
    # bad_channels is a list of broken channels in the map, where map corresponds to the electrode channels
      - ntrode_id: 1 
        probe_id: 0 
        bad_channels: [0,2]
        map:  
          0: 0
          1: 1
          2: 2
          3: 3
      - ntrode_id: 2
        probe_id: 0
        bad_channels: [0,2]
        map:
          0: 4
          1: 5
          2: 6
          3: 7
    ```
5. Probe.yml description:
   ```
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
            rel_x: 0
            rel_y: 0
            rel_z: 0
          - id: 1
            rel_x: 0
            rel_y: 0
            rel_z: 0
   ```
6. Set up paths to metadata and probe `yaml` files, which corresponds to the experiment you are going to process.
   ```bash
   metadata = MetadataManager('../test/datamigration/res/metadata.yml',
                         ['../test/datamigration/res/probe1.yml',
                          '../test/datamigration/res/probe2.yml',
                          '../test/datamigration/res/probe3.yml'
                         ])
   ```
7. Input files `metadata.yml` as well as `probe[1-N].yml` are validated against rec files headers.

8. Initialize RawToNWBBuilder, which requires `animal_name`, `data_path` and `dates` which exist in your experiment folder.
   ```bash
   builder = RawToNWBBuilder(animal_name='beans',
                             data_path='../test/test_data/',
                             dates=['20190718'],
                             nwb_metadata=metadata,
                             output_path='/out/nwb'
                             )
   ```
   raw_to_nwb_builder arguments

      **data_path** = `string` path to the parent folder of animal_name

      **animal_name** = `string` name of the folder that contain few dates-folders

      **dates** = `list of strings` names of folders that contain experiment data

      **nwb_metadata** = `MetadataManager` object with metadata.yml and probes.yml

      **output_path** = `string` path specifying location and name of result file (dafault 'output.nwb')</br>

      **extract_analog** = `boolean` flag specifying if analog data should be extracted from raw (default False)</br>

      **extract_spikes** = `boolean` flag specifying if spikes data should be extracted from raw (default False)</br>

      **extract_lfps** = `boolean` flag specifying if lfp data should be extracted from raw (default False)</br>

      **extract_dio** = `boolean` flag specifying if dio data should be extracted from raw (default True)</br>

      **extract_mda** = `boolean` flag specifying if mda data should be extracted from raw (default True)</br>

      **parallel_instances** = `int` number of threads, optimal value highly depends on hardware (default 4)</br>
      
      **overwrite** = `boolean`  If true, will overwrite existing files. (default True)</br>
      
      **analog_export_args** = `tuple of strings` path to rec header file which overrides all headers existing in rec binary files e.g `_DEFAULT_ANALOG_EXPORT_ARGS = ('-reconfig', str(path) + '/test/datamigration/res/reconfig_header.xml')`</br>

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

12. `fldatamigration.log` contains useful information about processing phases as well as all of the exceptions and errors.

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




