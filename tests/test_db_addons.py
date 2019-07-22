from conftest import GeoLibTestInstance as core_test

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_engine_session():
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
    return sessionmaker(engine)(), engine


def test_a():
    a, b = get_engine_session()
    print(a)
    assert False

def test_b():
    a, b = get_engine_session()
    print(a)
    assert False