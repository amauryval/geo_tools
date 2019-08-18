
import psycopg2

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy import exc

from sqlalchemy_utils import database_exists
from sqlalchemy_utils import create_database
from sqlalchemy_utils import drop_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema

from ..core.geotoolscore import GeoToolsCore


class DataBaseAddons(GeoToolsCore):
    """
    Class : DataBaseAddons
    """
    def __init__(self):
        super().__init__()

    def _sqlalchemy_engine(self, host, database, username, password, port=5432):
        """
        sql_engine

        :param data_base: str
        :param user: str
        :param password: str
        :param host: str
        :param port: int, default 5432
        :param print_conn: boolean,
        :return:
        """

        use_batch_mode = True
        client_encoding = 'utf8'
        pool_size = 100
        max_overflow = 0

        url_postgres = f'postgresql://{username}:{password}@{host}:{port}/{database}'

        engine = create_engine(
            url_postgres,
            client_encoding=client_encoding,
            use_batch_mode=use_batch_mode,
            pool_size=pool_size,
            max_overflow=max_overflow
        )
        session = sessionmaker(engine)

        return session(), engine

    def __get_metadata(self, engine, schema):

        metadata = MetaData(
            bind=engine,
            schema=schema
        )
        self.info("Get meta schema %s" % (metadata))
        return metadata

    def sql_alchemy_db_init(self, host, database, username, password, port, extensions, overwrite=False, verbose=False):
        """
        init_database

        :type host: str
        :type port: int
        :type database: str
        :type username: str
        :type password: str
        :type overwrite: bool, default: false
        :return: session, engine
        """
        try:
            session, engine = self._sqlalchemy_engine(host, database, username, password, port)

            if verbose:
                self.info(f'Engine OK : {engine}')

        except Exception as ex:
            self.warning(f'{type(ex).__name__}: Engine NOK (Arguments: {ex.args})')
            raise ex

        try:
            if database_exists(engine.url):
                self.warning(f'Database {database} exists')
                if overwrite:
                    self.warning(f'Overwrite is True => Database {database} dropped')
                    drop_database(engine.url)
                    self.sql_alchemy_db_init(
                        host,
                        database,
                        username,
                        password,
                        port,
                        extensions,
                        overwrite,
                        verbose=False
                    )

            else:
                self.info(f'Database : {database} created!')
                create_database(engine.url)

                for extension in extensions:
                    try:
                        engine.execute('create extension %s' % extension)
                    except Exception as err:
                        self.warning(f"{type(err).__name__}: extensions declaration error (args: {err.args})")

        except exc.OperationalError as ex:
            self.warning(f'Oops default db postgres does not exists : {ex}')

        return session, engine

    def psycopg2_connection(self, host, database, username, password, port=5432):
        """

        :type database: string
        :type username: string
        :type host: string
        :type password: string
        :type port: int, default 5432
        :return:
        """
        connection = psycopg2.connect(
            dbname=database,
            user=username,
            host=host,
            password=password,
            port=port
        )

        return connection

    def schema_init(self, engine, schema):
        """
        init_schema

        :param engine:
        :param schema: str
        :return: str
        """
        is_exists = False
        try:
            engine.execute(CreateSchema(schema))
            self.info(f'Creating {schema} schema')

        except:
            self.info(f'Schema {schema} already exists')
            is_exists = True

        return is_exists



    def sql_table_by_name(self, engine, schema, table):
        """
        get_sql_table

        :param engine:
        :type schema: str
        :type table: str
        :return:
        """

        metadata = self.__get_metadata(engine, schema)

        try:
            autoload = True
            return Table(
                table,
                metadata,
                autoload=autoload,
                autoload_with=engine
            )

        except exc.NoSuchTableError as _:
            return None

    def is_sql_table_filled(self, engine, schema, table):

        table_found = self.sql_table_by_name(engine, schema, table)
        if table_found is not None:
            rows_count = engine.execute(
                select([func.count()]).select_from(
                    table_found
                )).scalar()
            print(rows_count)
            if rows_count > 0:
                return True

            return False

        return None
