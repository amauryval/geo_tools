from ..core.geotoolscore import GeoToolsCore

import pandas as pd
import geopandas as gpd

from sqlalchemy import select

from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import MultiPoint
from shapely.geometry import MultiLineString
from shapely.geometry import MultiPolygon
from shapely.geometry import GeometryCollection


class PandasAddons(GeoToolsCore):

    def __init__(self):
        super().__init__()

    def df_from_table(self, engine, meta, schema, table):
        """
        df_from_table

        :param engine:
        :param meta:
        :param schema: str
        :param table: str
        """

        metadata = self.get_metadata(engine, schema)
        try:
            self.info(f"Load Dataframe from db: '{schema}'.{table}")
            table_conn = metadata.tables[f"{schema}.{table}"]
            return pd.read_sql_query(
                select([table_conn])
                , con=engine
            )

        except Exception as ex:
            raise ex

    def gdf_from_table(self, engine, schema, table, geom_col="geometry"):
        """
        gdf_from_table

        :type engine:
        :type schema: str
        :type table: str
        :type geom_col: str, default: geometry
        :return:
        """

        metadata = self.get_metadata(engine, schema)
        try:
            self.logger.info(f"Load Geodataframe from db: '{schema}'.{table}")
            table_conn = metadata.tables[f"{schema}.{table}"]
            return gpd.GeoDataFrame.from_postgis(
                "SELECT * FROM " + str(table_conn),
                con=engine,
                geom_col=geom_col
            )

        except Exception as ex:
            raise ex

    def layer_files_to_gdf(self, files, polygon=None, fields_to_keep=None):
        """
        layer_files_to_gdf

        :type files: list of str
        :type polygon: shapely.geometry.Polygon
        :type fields_to_keep: list
        :return: geopandas.geodataframe
        """
        polygon_bounds = None
        if polygon is not None:
            polygon_bounds = polygon.bounds

        if fields_to_keep is None:
            fields_to_keep = (slice(None))

        geodataframe = pd.concat([
            gpd.read_file(file_path, bbox=polygon_bounds)[fields_to_keep]
            for file_path in files
        ])

        if polygon is not None:
            # TODO optimize
            geodataframe = geodataframe.loc[geodataframe['geometry'].intersects(polygon)]

        return geodataframe

    def shapely_geom_to_gdf(self, geometry, in_epsg=None, out_epsg=None):
        """
        shapely_geom_to_gdf

        :param geometry:
        :param in_epsg:
        :param out_epsg:
        :return:
        """

        if isinstance(geometry, (MultiPoint, MultiLineString, MultiPolygon, GeometryCollection)):
            geometry = [[geom] for geom in geometry]

        elif isinstance(geometry, (Point, LineString, Polygon)):
            geometry = [[geometry]]

        dataframe = pd.DataFrame.from_records(geometry, columns=['geometry'])
        geodataframe = gpd.GeoDataFrame(
            dataframe,
            geometry=dataframe['geometry']
        )

        if in_epsg is not None:
            geodataframe = geodataframe.crs({'init': 'epsg:%s' % in_epsg})

        if out_epsg is not None:
            geodataframe = geodataframe.to_crs({'init': 'epsg:%s' % out_epsg})

        return geodataframe