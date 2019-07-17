from shapely.wkt import loads

from conftest import GeoLibTestInstance as core_test

import pytest


def test_ogr_reprojection_same_epsg(point):
    point_reprojection = core_test().ogr_reprojection(point, 4326, 4326)
    assert point_reprojection.equals(point)


def test_pyproj_reprojection_same_epsg(point):
    point_reprojection = core_test().pyproj_reprojection(point, 4326, 4326)
    assert point_reprojection.equals(point)
