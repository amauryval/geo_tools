from shapely.wkt import loads

from conftest import GeoLibTestInstance as core_test

import pytest


def test_ogr_reprojection(point):
    point_reprojection = core_test().ogr_reprojection(point, 4326, 2154)
    assert point_reprojection.equals(loads('POINT Z (4173176.90409232 2897168.59708177 5)'))


def test_pyproj_reprojection(point):
    point_reprojection = core_test().pyproj_reprojection(point, 2154, 4326)
    assert point_reprojection.equals(loads('POINT Z (4173176.90409232 2897168.59708177 5)'))
