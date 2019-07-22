
import psycopg2

from sqlalchemy import create_engine

from sqlalchemy import exc
from sqlalchemy_utils import database_exists
from sqlalchemy_utils import create_database
from sqlalchemy_utils import drop_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema


class DataBaseAddons:
    """
    Class : DataBaseAddons
    """

    def __sqlalchemy_engine(self, host, database, username, password, port=5432):
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
            session, engine = self.__sqlalchemy_engine(host, database, username, password, port)

            if verbose:
                print("Engine OK : {engine}")

        except Exception as ex:
            print(f"{type(ex).__name__}: Engine NOK (Arguments: {ex.args})")
            raise ex

        try:
            if database_exists(engine.url):
                print(f'Database {database} exists')
                if overwrite:
                    print(f'Overwrite is True => Database {database} dropped')
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
                print(f'Database : {database} created!')
                create_database(engine.url)

                for extension in extensions:
                    try:
                        engine.execute('create extension %s' % extension)
                    except Exception as err:
                        print(f"{type(err).__name__}: extensions declaration error (args: {err.args})")

        except exc.OperationalError as ex:
            print(f'Oops default db postgres does not exists : {ex}')

        return session, engine

    def psycopg2_connection(self, dbname, user, host, password, port=5432):
        """

        :type dbname: string
        :type user: string
        :type host: string
        :type password: string
        :type port: int, default 5432
        :return:
        """
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            host=host,
            password=password,
            port=port
        )

        return connection

    def schema_init(self, engine, schemas):
        """
        init_schema

        :param engine:
        :param schemas: list(str)
        :return: str
        """

        for schema in schemas:
            try:
                engine.execute(CreateSchema(schema))
                print(f'Creating {schema} schema')

            except:
                print(f'Schema {schema} already exists')
