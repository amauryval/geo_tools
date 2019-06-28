# geo_tools

## Shapely geometry functions

* remove Z coordinates on your geometry
* get crossroads, dead ends and section nodes from a MultiLinestring
* convert your geometry to LineString (only 2 coordinates)
* convert your geometry to points
* Drop duplicate geometries
* Create points along line features by choosing a ratio
* Cut line features at specifics point
* convert geometry to bokeh format (use geopandas and apply method)
* Fill holes on Polygon, MultiPolygon, and GeometryCollection
* Convert (Multi)Polygon holes to MultiPolygons
* Compute side buffer on LineString and MultiLineString

## Reprojection functions

* reproject with pyproj
* reproject with ogr

## More soon !

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

## Check examples
```
jupyter notebook
```

Then check Jupyter Notebook in 'examples' directory

## Run tests
```
python -m pytest tests
```
