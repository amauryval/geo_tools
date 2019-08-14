import pytest

from fixtures.geometry import *
from fixtures.db import *

from geotools.geotools import GeoTools


#######################################
# CLASS FOR TEST
class GeoLibTestInstance(GeoTools):

    def __init__(self, logger_dir=None):
        super().__init__(logger_dir=None)


def pytest_sessionstart():
    SqlAlchemySession().create_db_and_table()

def pytest_sessionfinish(session, exitstatus):
    SqlAlchemySession()._drop_db()
