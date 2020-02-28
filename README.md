# LorenFranksDataMigration
LorenFranksDataMigration is a python package that converts SpikeGadgets rec files to NWB files.
It converts data from `/raw` folder to `.nwb` file.
It utilizes rec_to_binaries package.</br>
https://github.com/LorenFrankLab/rec_to_binaries</br>

### Prerequisites
1. Before using the package you have to install Spike Gadgets
   https://bitbucket.org/mkarlsso/trodes/downloads/
2. Add SpikeGadgets to path.
   If Spike Gadgets is in default location: 
   ```bash
   export PATH="$HOME/SpikeGadgets/:$PATH"'
   ```
3. If conda isn't installed, download miniconda from</br>
   https://docs.conda.io/en/latest/miniconda.html</br>
4. LFDataMigration Installation
   ```bash
   conda ....
   ```
5. Create conda environment. 
   ```bash
   conda env create -f <path-to-environment.yml-file>
   ```
   if used from `/LorenFranksDataMigration`
   ```bash
   conda env create -f environment.yml
   ```
6. jupyter notebook installation
   ```bash
   pip install jupyter notebook
   ```

### Usage
1. In terminal navigate to `/LorenFranksDataMigration/src/notebooks`
2. run jupyter notebook
   ```bash
   jupyter notebook
   ```
3. In jupyter notebook change following paths to your metadata and probe `.yml` file paths.
   ```bash
   metadata = NWBMetadata('../test/datamigration/res/metadata.yml',
                         ['../test/datamigration/res/probe1.yml',
                          '../test/datamigration/res/probe2.yml',
                          '../test/datamigration/res/probe3.yml'
                         ])
   ```
4. In
   ```bash
   builder = RawToNWBBuilder(animal_name='beans',
                             data_path='../test/test_data/',
                             dates=['20190718'],
                             nwb_metadata=metadata,
                             )
   ```
   change `animal_name`, `data_path` and `dates` to correct ones
   
   
5. Make sure that the data structure in given directory (in this case `test_data`)
   is similar to this one
   ```bash
    --test_data
      |
      `-- lotus
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
   
   #todo  please add preprocessing folder structure and explain it.
6. Run the code (depending of the size of experiment datasets it may take from a few minutes to even several hours)
7. Transformation is completed, nwb file, has been created in a given directory.
   
   
   
   
