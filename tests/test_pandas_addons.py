from conftest import GeoLibTestInstance as core_test

import pytest

from fixtures.db import SqlAlchemySession

import pandas as pd
import geopandas as gpd


def test_pandas_df_from_sql_table_not_existing_table(schema_name_not_existing, table_name_not_existing):

    host, database, username, password, port, _ = SqlAlchemySession()._prepare_input()
    _, sql_alchemy_engine = core_test()._sqlalchemy_engine(host, database, username, password, port)
    data = core_test().df_from_sql_table(sql_alchemy_engine, schema_name_not_existing, table_name_not_existing)
    assert data is None

def test_pandas_df_from_sql_table_existing_table(schema_name_existing, table_name_existing):

    host, database, username, password, port, _ = SqlAlchemySession()._prepare_input()
    _, sql_alchemy_engine = core_test()._sqlalchemy_engine(host, database, username, password, port)
    data = core_test().df_from_sql_table(sql_alchemy_engine, schema_name_existing, table_name_existing)
    assert isinstance(data, pd.DataFrame)
    assert len(data) == 1

def test_geopandas_df_from_sql_table_existing_table(schema_name_existing, table_name_existing):

    host, database, username, password, port, _ = SqlAlchemySession()._prepare_input()
    _, sql_alchemy_engine = core_test()._sqlalchemy_engine(host, database, username, password, port)
    data = core_test().df_from_sql_table(sql_alchemy_engine, schema_name_existing, table_name_existing, geo_table=True)
    assert isinstance(data, gpd.geodataframe.GeoDataFrame)
    assert len(data) == 1
