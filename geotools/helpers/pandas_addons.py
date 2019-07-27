import pandas as pd
import geopandas as gpd

from sqlalchemy import MetaData
from sqlalchemy import select

import geoalchemy2
from geoalchemy2.types import Geometry


class PandasAddons:
    """
    Class : PandasAddons
    """

    def df_from_sql_table(self, engine, schema, table, geo_table=False, column_geom='geometry'):

        db_metadata = MetaData(bind=engine, schema=schema)
        db_metadata.reflect(engine)

        if len(db_metadata.tables) == 0:
            print(f'Table do not exist: "{schema}".{table}')
            return None

        table_connection = db_metadata.tables[f'{schema}.{table}']
        table_query = select([table_connection])
        table_column_type = {col.name: col.type for col in table_query.columns}

        if not geo_table:
            print(f'Loading dataframe from table: "{schema}".{table}')
            data = pd.read_sql_query(
                table_query,
                con=engine
            )

            geometry_column_found = list(filter(lambda x: isinstance(x[-1], geoalchemy2.types.Geometry), table_column_type.items()))
            if len(geometry_column_found) > 0:
                print(f'warning : geom column exists : {", ".join(map(str, geometry_column_found))}')

        else:
            print(f'Loading geodataframe from table: "{schema}".{table}')
            data = gpd.GeoDataFrame.from_postgis(
                "SELECT * FROM " + str(table_connection),
                con=engine,
                geom_col=column_geom
            )


        return data

