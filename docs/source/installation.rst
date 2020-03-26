Installation
===================
.. toctree::
   :maxdepth: 3

Prerequisites
^^^^^^^^^^^^^^^

For Users
+++++++++++++++++++++
1. Install Spike Gadgets
   https://bitbucket.org/mkarlsso/trodes/downloads/
2. Add SpikeGadgets to path.
   If Spike Gadgets is in default location:
   ```bash
   export PATH="$HOME/SpikeGadgets/:$PATH"'
   ```
3. Download miniconda from</br>
   https://docs.conda.io/en/latest/miniconda.html</br>
4. Download `fldatamigration.yml` from https://anaconda.org/NovelaKRK/fldatamigration/files
5. Build fldatamigration environment:
   ```bash
   conda env create -f fldatamigration.yml
   ```
6. Install Jupyter notebook
   ```bash
   pip install jupyter notebook
   ```


For Developers
+++++++++++++++++++++
1. Install Spike Gadgets
   https://bitbucket.org/mkarlsso/trodes/downloads/
2. Add SpikeGadgets to path.
   If Spike Gadgets is in default location:
   ```bash
   export PATH="$HOME/SpikeGadgets/:$PATH"'
   ```
3. Download miniconda from
</br>https://docs.conda.io/en/latest/miniconda.html</br>
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
7. Documentation can be view with pdoc server
   ```bash
   pdoc -b
   ```