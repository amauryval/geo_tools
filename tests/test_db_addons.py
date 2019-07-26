from conftest import GeoLibTestInstance as core_test

import pytest

from sqlalchemy.orm.session import Session
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.schema import Table

from psycopg2.extensions import connection

from sqlalchemy_utils import drop_database


def get_url_db():
    username = 'postgres'
    password = 'postgres'
    host = 'localhost'
    port = 5432
    database = 'geo_tools_tests'
    extensions = ['btree_gist', 'postgis']

    return host, database, username, password, port, extensions


def test_get_sql_alchemy_engine():
    host, database, username, password, port, _ = get_url_db()
    sql_alchemy_session, sql_alchemy_engine = core_test()._sqlalchemy_engine(host, database, username, password, port)
    assert isinstance(sql_alchemy_session, Session)
    assert isinstance(sql_alchemy_engine, Engine)

def test_psycopg2_connection():
    host, database, username, password, port, _ = get_url_db()
    db_connection = core_test().psycopg2_connection(host, database, username, password, port)
    assert isinstance(db_connection, connection)

def test_new_schema_init(schema_name_not_existing):
    host, database, username, password, port, extensions = get_url_db()
    _, sql_alchemy_engine = core_test().sql_alchemy_db_init(host, database, username, password, port, extensions, overwrite=False, verbose=False)
    is_exists = core_test().schema_init(sql_alchemy_engine, schema_name_not_existing)
    assert is_exists == False

def test_exisiting_schema_init(schema_name_existing):
    host, database, username, password, port, extensions = get_url_db()
    _, sql_alchemy_engine = core_test().sql_alchemy_db_init(host, database, username, password, port, extensions, overwrite=False, verbose=False)
    is_exists = core_test().schema_init(sql_alchemy_engine, schema_name_existing)
    assert is_exists == True

def test_get_existing_sql_table(schema_name_existing, table_name_existing):
    host, database, username, password, port, extensions = get_url_db()
    _, sql_alchemy_engine = core_test().sql_alchemy_db_init(host, database, username, password, port, extensions, overwrite=False, verbose=False)
    table = core_test().sql_table_by_name(sql_alchemy_engine, schema_name_existing, table_name_existing)
    assert isinstance(table, Table)

def test_get_not_existing_sql_table(schema_name_existing, table_name_not_existing):
    host, database, username, password, port, extensions = get_url_db()
    _, sql_alchemy_engine = core_test().sql_alchemy_db_init(host, database, username, password, port, extensions, overwrite=False, verbose=False)
    table = core_test().sql_table_by_name(sql_alchemy_engine, schema_name_existing, table_name_not_existing)
    assert table is None

def test_get_existing_sql_table_is_filled(schema_name_existing, table_name_existing):
    host, database, username, password, port, extensions = get_url_db()
    _, sql_alchemy_engine = core_test().sql_alchemy_db_init(host, database, username, password, port, extensions, overwrite=False, verbose=False)
    print(sql_alchemy_engine)
    is_filled = core_test().is_sql_table_filled(sql_alchemy_engine, schema_name_existing, table_name_existing)
    assert is_filled == True

def test_get_not_existing_sql_table_is_filled(schema_name_existing, table_name_not_existing):
    host, database, username, password, port, extensions = get_url_db()
    _, sql_alchemy_engine = core_test().sql_alchemy_db_init(host, database, username, password, port, extensions, overwrite=False, verbose=False)
    is_filled = core_test().is_sql_table_filled(sql_alchemy_engine, schema_name_existing, table_name_not_existing)
    assert is_filled is None

# These tests need to run at the end #
def test_sql_alchemy_db_init_not_overwrited():
    host, database, username, password, port, extensions = get_url_db()
    sql_alchemy_session, sql_alchemy_engine = core_test().sql_alchemy_db_init(host, database, username, password, port, extensions, overwrite=False, verbose=False)
    assert isinstance(sql_alchemy_session, Session)
    assert isinstance(sql_alchemy_engine, Engine)

def test_sql_alchemy_db_init_overwrited():
    host, database, username, password, port, extensions = get_url_db()
    sql_alchemy_session, sql_alchemy_engine = core_test().sql_alchemy_db_init(host, database, username, password, port, extensions, overwrite=True, verbose=False)
    assert isinstance(sql_alchemy_session, Session)
    assert isinstance(sql_alchemy_engine, Engine)

def test_sql_alchemy_db_init_new_db(new_db_name):
    host, database, username, password, port, extensions = get_url_db()
    database = new_db_name
    sql_alchemy_session, sql_alchemy_engine = core_test().sql_alchemy_db_init(host, database, username, password, port, extensions, overwrite=True, verbose=False)
    assert isinstance(sql_alchemy_session, Session)
    assert isinstance(sql_alchemy_engine, Engine)
    drop_database(sql_alchemy_engine.url)
# These tests need to run at the end #