# geo_tools

A geographic (and more...) toolbox

*CircleCI tests : [![CircleCI](https://circleci.com/gh/yruama42/geo_tools.svg?style=svg)](https://circleci.com/gh/yruama42/geo_tools)*

## Shapely geometry methods

* Remove Z coordinates on your geometry
* Get crossroads, dead ends and section nodes from a MultiLinestring
* Convert your geometry to LineString
* Convert your geometry to points
* Drop duplicate geometries
* Create points along line features by choosing a ratio
* Cut line features at specifics point
* Convert geometry to bokeh format
* Fill holes on Polygon, MultiPolygon, and GeometryCollection
* Convert Polygon holes to MultiPolygons
* Compute side buffer on LineString and MultiLineString

## Reprojection methods

* reproject with pyproj
* reproject with ogr

## Database methods
* Easy use of SqlAlchemy to connect/create/overwrite on a PostgreSQL database
* check table (filled or not, existing or not...)
* ...
* To be continued !...

## More soon !

## Installation

with anaconda3
```
conda create -y --name geo_tools python=3.6
source activate geo_tools
conda config --add channels conda-forge
conda config --set channel_priority strict
conda install -y -q --name geo_tools --file requirements.txt
```

## How to use it

In your script.py:

```python
from geotools.geotools import GeoTools

class MyBeautifulClass(GeoTools):
    def __init__(self, logger_dir=None):
        super().__init__(logger_dir=logger_dir)

    def run(self):
        # call all GeoTools functions
        self.info('Hello')
```

## Check examples

Check Jupyter Notebook in 'examples' directory

in your terminal Anaconda Prompt
```
jupyter notebook
```

## Run tests

in your terminal Anaconda Prompt
```
python -m pytest tests
```
