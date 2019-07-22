import pytest

from fixtures.geometry import *
from fixtures.db import *

from geotools.core import GeoTools

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database
from sqlalchemy.schema import CreateSchema


from sqlalchemy_utils import drop_database


#######################################
# CLASS FOR TEST
class GeoLibTestInstance(GeoTools):

    def __init__(self):
        super().__init__()


def pytest_sessionstart():
    # TODO add url in var ENV
    use_batch_mode = True
    client_encoding = 'utf8'
    pool_size = 100
    max_overflow = 0

    username = 'postgres'
    password = 'postgres'
    host = 'localhost'
    port = 5432
    database = 'geo_tools_tests'
    url_postgres = f'postgresql://{username}:{password}@{host}:{port}/{database}'

    engine = create_engine(
        url_postgres,
        client_encoding=client_encoding,
        use_batch_mode=use_batch_mode,
        pool_size=pool_size,
        max_overflow=max_overflow
    )
    create_database(engine.url)

    #extensions
    engine.execute('create extension Postgis')
    engine.execute('create extension btree_gist')

    # schema
    schemas = Base.metadata._schemas
    for schema in schemas:
        engine.execute(CreateSchema(schema))

    # table
    Base.metadata.create_all(engine)


def pytest_sessionfinish(session, exitstatus):
    # TODO add url in var ENV
    username = 'postgres'
    password = 'postgres'
    host = 'localhost'
    port = 5432
    database = 'geo_tools_tests'
    url_postgres = f'postgresql://{username}:{password}@{host}:{port}/{database}'

    drop_database(url_postgres)