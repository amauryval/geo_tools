# geo_tools [TODO]

Shapely geometry functions


## Installation

with anaconda3
```
conda env create -f geo_tools_conda_env.yml
```

## How to use it

In your script.py:

```python
from geotools.core import GeoTools

class MyBeautifulClass(GeoTools):

    def __init__(self):
        super().__init__()
    
    def run(self):
        # call GeoTools functions
        self.remove_z_geom(my_shapely_geometry)

```

## Run tests
```
python -m pytest tests
```
