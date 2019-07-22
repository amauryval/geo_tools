import pytest

import re

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database
from sqlalchemy.schema import CreateSchema

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from sqlalchemy.dialects.postgresql import TSRANGE
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry
from sqlalchemy.sql import func

Base = declarative_base()


@as_declarative()
class Base:

    _session = None

    @declared_attr
    def __tablename__(cls):
        return re.sub('([A-Z])', ' \g<1>', cls.__name__).strip().replace(' ', '_').lower()

    id = Column(Integer, primary_key=True)
    validity_range = Column(TSRANGE(), index=True)
    created_at = Column(DateTime(timezone=False), server_default=func.now())


class ALittleThing(Base):
    __table_args__ = (
        {"schema": "stuff"}
    )

    name = Column(String)
    category = Column(String, index=True)
    details = Column(JSONB)
    geometry = Column(Geometry('POINT', 4326))


# @pytest.fixture(scope='session', autouse=True)
# def fake_db():
#     # TODO add settings.json
#     use_batch_mode = True
#     client_encoding = 'utf8'
#     pool_size = 100
#     max_overflow = 0
#
#     username = 'postgres'
#     password = 'postgres'
#     host = 'localhost'
#     port = 5432
#     database = 'geo_tools_tests'
#     url_postgres = f'postgresql://{username}:{password}@{host}:{port}/{database}'
#
#     engine = create_engine(
#         url_postgres,
#         client_encoding=client_encoding,
#         use_batch_mode=use_batch_mode,
#         pool_size=pool_size,
#         max_overflow=max_overflow
#     )
#     create_database(engine.url)
#
#     #extensions
#     engine.execute('create extension Postgis')
#     engine.execute('create extension btree_gist')
#
#     # schema
#     schemas = Base.metadata._schemas
#     for schema in schemas:
#         engine.execute(CreateSchema(schema))
#
#     # table
#     Base.metadata.create_all(engine)
#
#     return sessionmaker(engine)(), engine