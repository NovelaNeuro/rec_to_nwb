# lfdatamigration
lfdatamigration is a python package for converting SpikeGadgets rec files to NWB files.
It converts experiment data from `/raw` folder to `.nwb` file.
It utilizes rec_to_binaries package for preprocessing phase.</br>
https://github.com/LorenFrankLab/rec_to_binaries</br>

### Prerequisites
### For users
1. Install Spike Gadgets
   https://bitbucket.org/mkarlsso/trodes/downloads/
2. Add SpikeGadgets to path.
   If Spike Gadgets is in default location:
   ```bash
   export PATH="$HOME/SpikeGadgets/:$PATH"'
   ```
3. Download miniconda from</br>
   https://docs.conda.io/en/latest/miniconda.html</br>
4. Download `lfdatamigration.yml` from https://anaconda.org/NovelaKRK/lfdatamigration/files
5. Build lfdatamigration environment:
   ```bash
   conda env create -f lfdatamigration.yml
   ```
6. Install Jupyter notebook
   ```bash
   pip install jupyter notebook
   ```

### For developers
1. Install Spike Gadgets
   https://bitbucket.org/mkarlsso/trodes/downloads/
2. Add SpikeGadgets to path.
   If Spike Gadgets is in default location:
   ```bash
   export PATH="$HOME/SpikeGadgets/:$PATH"'
   ```
3. Download miniconda from</br>
   https://docs.conda.io/en/latest/miniconda.html</br>
4. clone repository
   ```bash
   git clone https://github.com/NovelaNeuro/lfdatamigration.git

   cd lfdatamigration/lf
   ```
5. Create conda environment.
   ```bash
   conda env create -f environment.yml
   ```
6. jupyter notebook installation
   ```bash
   pip install jupyter notebook
   ```
7. Documentation can be view with pdoc server
   ```bash
   pdoc -b
   ```

# How to use it
1. Download example notebook file from
   https://anaconda.org/NovelaKRK/nwb_generation/notebook
2. In terminal navigate to notebook file location
3. Run jupyter notebook
   ```bash
   jupyter notebook
   ```
4. Set up paths to metadata and probe `yaml` files, which corresponds to the experiment you are going to process.
   ```bash
   metadata = MetadataManager('../test/datamigration/res/metadata.yml',
                         ['../test/datamigration/res/probe1.yml',
                          '../test/datamigration/res/probe2.yml',
                          '../test/datamigration/res/probe3.yml'
                         ])
   ```
5. Input files `metadata.yml` as well as `probe[1-N].yml` are validated against rec files headers.

6. Initialize RawToNWBBuilder, which requires `animal_name`, `data_path` and `dates` which exist in your experiment folder.
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

      **extract_time** = `boolean` flag specifying if time data should be extracted from raw (default True)</br>

      **extract_mda** = `boolean` flag specifying if mda data should be extracted from raw (default True)</br>

      **parallel_instances** = `int` number of threads, optimal value highly depends on hardware (default 4)</br>

7. Make sure that the data structure in given directory (in that case `test_data`)
   looks similar to following example:
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

8. Double check if there is enough disc space on your Laptop/PC.

9. Run processing (generation may take from mins to even hours and it depends on the size of experiment datasets).

10. `lfdatamigration.log` contains useful information about processing phases as well as all of the exceptions and errors.

11. Example structure of preprocessed experiment data
   ```bash
   |-- beans
   |   |-- preprocessing
   |   |   |
   |   |   `-- 20190718
   |   |       |-- 20190718_beans_01_s1.1.pos
   |   |       |   |-- 20190718_beans_01_s1.1.pos_cameraHWFrameCount.dat
   |   |       |   |-- 20190718_beans_01_s1.1.pos_online.dat
   |   |       |   `-- 20190718_beans_01_s1.1.pos_timestamps.dat
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
   |   |       |   `-- 20190718_beans_01_s1.timestamps.dat
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
   |   |       |   `-- 20190718_beans_01_s1.exportdio.log
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
   |   |       |   `-- 20190718_beans_01_s1.timestamps.dat
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
   |   |       |   `-- 20190718_beans_01_s1.timestamps.mda
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
   |   |       |   `-- 20190718_beans_01_s1.spikes_nt9.dat
   |   |       `-- 20190718_beans_01_s1.time
   |   |           |-- 20190718_beans_01_s1.continuoustime.dat
   |   |           |-- 20190718_beans_01_s1.exporttime.log
   |   |           `-- 20190718_beans_01_s1.time.dat
   |   `-- raw
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
When processing completes, a nwb file is created in the output_path directory




