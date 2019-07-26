from shapely.wkt import loads

from conftest import GeoLibTestInstance as core_test

import pytest


def test_ogr_reprojection_same_epsg(point):
    point_reprojected = core_test().ogr_reprojection(point, 4326, 4326)
    assert point_reprojected.equals(point)


def test_pyproj_reprojection_same_epsg(point):
    point_reprojected = core_test().pyproj_reprojection(point, 4326, 4326)
    assert point_reprojected.equals(point)

def test_ogr_reprojection_diff_epsg(point):
    point_reprojected = core_test().ogr_reprojection(point, 4326, 2154)
    point_reprojected_revert = core_test().ogr_reprojection(point_reprojected, 2154, 4326)
    assert point_reprojected_revert.equals(point)

def test_pyproj_reprojection_diff_epsg(point):
    point_reprojected = core_test().pyproj_reprojection(point, 4326, 2154)
    point_reprojected_revert = core_test().pyproj_reprojection(point_reprojected, 2154, 4326)
    assert not point_reprojected_revert.equals(point)
    # Haha unbelievable, pyproj change coordinate precision when reprojecting data ! I don't like it !
