import pytest

import re

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database
from sqlalchemy_utils import drop_database
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


class SqlAlchemySession:

    def _prepare_input(self):
        # TODO add url in var ENV
        self._use_batch_mode = True
        self._client_encoding = 'utf8'
        self._pool_size = 100
        self._max_overflow = 0

        username = 'postgres'
        password = 'postgres'
        host = 'localhost'
        port = 5432
        database = 'geo_tools_tests'
        self._url_postgres = f'postgresql://{username}:{password}@{host}:{port}/{database}'

    def _create_db(self):
        self._engine = create_engine(
            self._url_postgres,
            client_encoding=self._client_encoding,
            use_batch_mode=self._use_batch_mode,
            pool_size=self._pool_size,
            max_overflow=self._max_overflow
        )
        self._session = sessionmaker(self._engine)()
        create_database(self._engine.url)

        # extensions
        self._engine.execute('create extension Postgis')
        self._engine.execute('create extension btree_gist')

    def _fill_db(self):

        feature = ALittleThing(
            name='name1',
            category='catego1',
            details=None,
            geometry=None,
        )
        self._session.add(feature)
        self._session.commit()

    def create_db_and_table(self):
        self._prepare_input()
        self._create_db()

        # schema
        schemas = Base.metadata._schemas
        for schema in schemas:
            self._engine.execute(CreateSchema(schema))

        # table
        Base.metadata.create_all(self._engine)

        self._fill_db()

    def _drop_db(self):
        self._prepare_input()
        drop_database(self._url_postgres)

@pytest.fixture()
def new_db_name():
    return 'geotools_new'

@pytest.fixture()
def schema_name_existing():
    return 'stuff'

@pytest.fixture()
def schema_name_not_existing():
    return 'new_stuff'

@pytest.fixture()
def table_name_not_existing():
    return 'a_new_little_thing'

@pytest.fixture()
def table_name_existing():
    return 'a_little_thing'
