conda create -y --name geo_tools python=3.6
conda config --add channels conda-forge
conda install -y -q --name geo_tools --file requirements.txt