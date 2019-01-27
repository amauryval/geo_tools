from shapely.geometry import LineString, MultiPoint, Point, MultiLineString, MultiPolygon, Polygon, GeometryCollection

from geotools.helpers.shapely_addons import GeometryTypeError

from conftest import GeoLibTestInstance as core_test

import pytest

#######################################
# GLOBAL FUNCTION FOR PY TESTS


def geom_3d_to_2d_geometry(geometry):
    geom = core_test().remove_z_geom(geometry)
    assert not geom.has_z


def geometry_to_points(geometry, drop_duplicates):
    geom = core_test().convert_geometry_to_points(geometry, drop_duplicates)
    assert isinstance(geom, MultiPoint)
    return geom.geoms


def count_values_by_type(values, type_to_check):
    types = list(map(lambda x: isinstance(x, type_to_check), values))
    return types.count(True)


def geometry_to_linestrings(geometry):
    geom = core_test().convert_geometry_to_simple_linestrings(geometry)
    assert isinstance(geom, MultiLineString)
    return geom.geoms

def geometry_to_intersection_nodes(geometry, mode):
    geom = core_test().get_intersection_nodes(geometry, mode)
    assert isinstance(geom, MultiPoint)
    return geom.geoms

def geometry_drop_duplicates(geometry):
    geom = core_test().drop_duplicates_geometry(geometry)
    assert isinstance(geom, type(geometry))
    return geom.geoms

def geometry_create_point_on_lines_feature(geometry):
    geom = core_test().create_point_along_line_features(geometry)
    assert isinstance(geom, MultiPoint)
    return geom.geoms

def geometry_cut_lines_features_at_points_ratio(geometry):
    geom = core_test().cut_line_features_at_points(geometry, ratio=0.5)
    assert isinstance(geom, MultiLineString)
    return geom.geoms

def geometry_cut_lines_features_at_points_from_points(geometry):
    # geom = Core().ogr_reprojection(geometry, 4326, 2154)
    points = core_test().create_point_along_line_features(geometry)
    geom = core_test().cut_line_features_at_points(geometry, ratio=None, points=points)
    assert isinstance(geom, MultiLineString)
    return geom.geoms

def geometry_get_geometry_coords(geometry):
    x = core_test().geometry_2_bokeh_format(geometry, 'x')
    y = core_test().geometry_2_bokeh_format(geometry, 'y')
    xy = core_test().geometry_2_bokeh_format(geometry, 'xy')
    return x, y, xy

def geometry_holes_computing(geometry):
    filled = core_test().fill_holes(geometry, 101)
    catched = core_test().get_holes(geometry, 100)
    return filled, catched

#######################################
# PY TESTS

# test_geom_3d_to_2d
def test_geom_3d_to_2d_point(point):
    geom_3d_to_2d_geometry(point)


def test_geom_3d_to_2d_multipoint(multipoint):
    geom_3d_to_2d_geometry(multipoint)


def test_geom_3d_to_2d_linestring(linestring):
    geom_3d_to_2d_geometry(linestring)


def test_geom_3d_to_2d_multilinestring(multilinestring):
    geom_3d_to_2d_geometry(multilinestring)


def test_geom_3d_to_2d_polygon(polygon):
    geom_3d_to_2d_geometry(polygon)


def test_geom_3d_to_2d_polygon_with_holes(polygon_with_holes):
    geom_3d_to_2d_geometry(polygon_with_holes)


def test_geom_3d_to_2d_multipolygon(multipolygon):
    geom_3d_to_2d_geometry(multipolygon)


def test_geom_3d_to_2d_multipolygon_with_holes(multipolygon_with_holes):
    geom_3d_to_2d_geometry(multipolygon_with_holes)


def test_geom_3d_to_2d_geometrycollection(geometrycollection):
    geom_3d_to_2d_geometry(geometrycollection)


# test_geometry_to_points
def test_point_to_points(point):
    geoms = geometry_to_points(point, False)
    assert len(geoms) == 1
    assert count_values_by_type(geoms, Point) == 1


def test_multipoint_to_points(multipoint):
    geoms = geometry_to_points(multipoint, False)
    assert len(geoms) == 2
    assert count_values_by_type(geoms, Point) == 2


def test_linestring_to_points(linestring):
    geoms = geometry_to_points(linestring, False)
    assert len(geoms) == 2
    assert count_values_by_type(geoms, Point) == 2


def test_multilinestring_to_points(multilinestring):
    geoms = geometry_to_points(multilinestring, False)
    assert len(geoms) == 14
    assert count_values_by_type(geoms, Point) == 14


def test_polygon_to_points(polygon):
    geoms = geometry_to_points(polygon, False)
    assert len(geoms) == 5
    assert count_values_by_type(geoms, Point) == 5


def test_polygon_with_holes_to_points(polygon_with_holes):
    geoms = geometry_to_points(polygon_with_holes, False)
    assert len(geoms) == 15
    assert count_values_by_type(geoms, Point) == 15


def test_multipolygon_to_points(multipolygon):
    geoms = geometry_to_points(multipolygon, False)
    assert len(geoms) == 10
    assert count_values_by_type(geoms, Point) == 10


def test_multipolygon_with_holes_to_points(multipolygon_with_holes):
    geoms = geometry_to_points(multipolygon_with_holes, False)
    assert len(geoms) == 15
    assert count_values_by_type(geoms, Point) == 15


def test_geometrycollection_to_points(geometrycollection):
    geoms = geometry_to_points(geometrycollection, False)
    assert len(geoms) == 54
    assert count_values_by_type(geoms, Point) == 54


def test_point_to_points_drop_duplicates(point):
    geoms = geometry_to_points(point, True)
    assert len(geoms) == 1
    assert count_values_by_type(geoms, Point) == 1


def test_multipoint_to_points_drop_duplicates(multipoint):
    geoms = geometry_to_points(multipoint, True)
    assert len(geoms) == 2
    assert count_values_by_type(geoms, Point) == 2


def test_linestring_to_points_drop_duplicates(linestring):
    geoms = geometry_to_points(linestring, True)
    assert len(geoms) == 2
    assert count_values_by_type(geoms, Point) == 2


def test_multilinestring_to_points_drop_duplicates(multilinestring):
    geoms = geometry_to_points(multilinestring, True)
    assert len(geoms) == 8
    assert count_values_by_type(geoms, Point) == 8


def test_polygon_to_points_drop_duplicates(polygon):
    geoms = geometry_to_points(polygon, True)
    assert len(geoms) == 4
    assert count_values_by_type(geoms, Point) == 4


def test_polygon_with_holes_to_points_drop_duplicates(polygon_with_holes):
    geoms = geometry_to_points(polygon_with_holes, True)
    assert len(geoms) == 12
    assert count_values_by_type(geoms, Point) == 12


def test_multipolygon_to_points_drop_duplicates(multipolygon):
    geoms = geometry_to_points(multipolygon, True)
    assert len(geoms) == 8
    assert count_values_by_type(geoms, Point) == 8

def test_multipolygon_with_holes_to_points_drop_duplicates(multipolygon_with_holes):
    geoms = geometry_to_points(multipolygon_with_holes, True)
    assert len(geoms) == 12
    assert count_values_by_type(geoms, Point) == 12

def test_geometry_drop_duplicates_multi_dupl(multipolygon_duplicate):
    geoms = geometry_drop_duplicates(multipolygon_duplicate)
    assert len(multipolygon_duplicate.geoms) == 2
    assert len(geoms) == 1

def test_geometry_drop_duplicates_multi_not_dupl(multipolygon):
    geoms = geometry_drop_duplicates(multipolygon)
    assert len(multipolygon.geoms) == 2
    assert len(geoms) == 2

def test_geometrycollection_to_points_drop_duplicates(geometrycollection):
    geoms = geometry_to_points(geometrycollection, True)
    assert len(geoms) == 37
    assert count_values_by_type(geoms, Point) == 37


# test_convert_geometry_to_linestrings
def test_point_to_linestrings(point):
    geometries = geometry_to_linestrings(point)
    assert len(geometries) == 0
    assert count_values_by_type(geometries, LineString) == 0


def test_multipoint_to_linestrings(multipoint):
    geometries = geometry_to_linestrings(multipoint)
    assert count_values_by_type(geometries, LineString) == 0
    assert len(geometries) == 0


def test_linestring_to_linestrings(linestring):
    geometries = geometry_to_linestrings(linestring)
    assert count_values_by_type(geometries, LineString) == 1
    assert len(geometries) == 1


def test_multilinestring_to_linestrings(multilinestring):
    geometries = geometry_to_linestrings(multilinestring)
    assert count_values_by_type(geometries, LineString) == 7
    assert len(geometries) == 7


def test_polygon_to_linestrings(polygon):
    geometries = geometry_to_linestrings(polygon)
    assert count_values_by_type(geometries, LineString) == 4
    assert len(geometries) == 4


def test_polygon_with_holes_to_linestrings(polygon_with_holes):
    geometries = geometry_to_linestrings(polygon_with_holes)
    assert count_values_by_type(geometries, LineString) == 12
    assert len(geometries) == 12



def test_multipolygon_to_linestrings(multipolygon):
    geometries = geometry_to_linestrings(multipolygon)
    assert count_values_by_type(geometries, LineString) == 8
    assert len(geometries) == 8


def test_multipolygon_with_holes_to_linestrings(multipolygon_with_holes):
    geometries = geometry_to_linestrings(multipolygon_with_holes)
    assert count_values_by_type(geometries, LineString) == 12
    assert len(geometries) == 12


def test_geometrycollection_to_linestrings(geometrycollection):
    geometries = geometry_to_linestrings(geometrycollection)
    assert count_values_by_type(geometries, LineString) == 39
    assert len(geometries) == 39


# test_geometry_to_linestrings
def test_get_dead_ends_intersection_nodes(multilinestring):
    geometries = geometry_to_intersection_nodes(multilinestring, 'dead_ends')
    assert len(geometries) == 5

def test_get_crossroads_intersection_nodes(multilinestring):
    geometries = geometry_to_intersection_nodes(multilinestring, 'crossroads')
    assert len(geometries) == 2

def test_get_sections_intersection_nodes(multilinestring):
    geometries = geometry_to_intersection_nodes(multilinestring, 'sections')
    assert len(geometries) == 1


# test_get_middle_point_on_linestring
def test_get_middle_point_on_linestring(linestring):
    geom = geometry_create_point_on_lines_feature(linestring)
    assert count_values_by_type(geom, Point) == 1
    assert geom[0].wkt == "POINT Z (-0.076 0.5349999999999999 0)"

def test_get_middle_point_on_linestring(linestring_not_simple):
    geom = geometry_create_point_on_lines_feature(linestring_not_simple)
    assert count_values_by_type(geom, Point) == 1


def test_get_middle_point_on_multilinestring(multilinestring):
    geometries = geometry_create_point_on_lines_feature(multilinestring)
    assert count_values_by_type(geometries, Point) == 7
    assert len(geometries) == 7


def test_get_middle_point_on_point(point):
    geometries = geometry_create_point_on_lines_feature(point)
    assert count_values_by_type(geometries, Point) == 0
    assert len(geometries) == 0


def test_get_middle_point_on_multipoint(multipoint):
    geometries = geometry_create_point_on_lines_feature(multipoint)
    assert count_values_by_type(geometries, Point) == 0
    assert len(geometries) == 0


def test_get_middle_point_on_polygon(polygon):
    geometries = geometry_create_point_on_lines_feature(polygon)
    assert count_values_by_type(geometries, Point) == 4
    assert len(geometries) == 4


def test_get_middle_point_on_multipolygon(multipolygon):
    geometries = geometry_create_point_on_lines_feature(multipolygon)
    assert count_values_by_type(geometries, Point) == 8
    assert len(geometries) == 8


def test_get_middle_point_on_multipolygon_with_holes(multipolygon_with_holes):
    geometries = geometry_create_point_on_lines_feature(multipolygon_with_holes)
    assert count_values_by_type(geometries, Point) == 12
    assert len(geometries) == 12


def test_get_middle_point_on_polygon_with_holes(polygon_with_holes):
    geometries = geometry_create_point_on_lines_feature(polygon_with_holes)
    assert count_values_by_type(geometries, Point) == 12
    assert len(geometries) == 12


def test_get_middle_point_on_geometrycollection(geometrycollection):
    geometries = geometry_create_point_on_lines_feature(geometrycollection)
    assert count_values_by_type(geometries, Point) == 39
    assert len(geometries) == 39


def test_geometry_cut_lines_features_at_points_ratio(point):
    geometries = geometry_cut_lines_features_at_points_ratio(point)
    assert count_values_by_type(geometries, LineString) == 0
    assert len(geometries) == 0

def test_geometry_cut_multipoint_features_at_points_ratio(multipoint):
    geometries = geometry_cut_lines_features_at_points_ratio(multipoint)
    assert count_values_by_type(geometries, LineString) == 0
    assert len(geometries) == 0

def test_geometry_cut_linestring_features_at_points_from_points(linestring):
    geometries = geometry_cut_lines_features_at_points_from_points(linestring)
    assert count_values_by_type(geometries, LineString) == 2
    assert len(geometries) == 2

def test_geometry_cut_multilinestring_features_at_points_from_points(multilinestring):
    geometries = geometry_cut_lines_features_at_points_from_points(multilinestring)
    assert count_values_by_type(geometries, LineString) == 14
    assert len(geometries) == 14

def test_geometry_cut_polygon_features_at_points_from_points(polygon):
    geometries = geometry_cut_lines_features_at_points_from_points(polygon)
    assert count_values_by_type(geometries, LineString) == 8
    assert len(geometries) == 8

def test_geometry_cut_polygon_with_holes_features_at_points_from_points(polygon_with_holes):
    geometries = geometry_cut_lines_features_at_points_from_points(polygon_with_holes)
    assert count_values_by_type(geometries, LineString) == 24
    assert len(geometries) == 24

def test_geometry_cut_multipolygon_features_at_points_from_points(multipolygon):
    geometries = geometry_cut_lines_features_at_points_from_points(multipolygon)
    assert count_values_by_type(geometries, LineString) == 16
    assert len(geometries) == 16

def test_geometry_cut_multipolygon_with_holes_features_at_points_from_points(multipolygon_with_holes):
    geometries = geometry_cut_lines_features_at_points_from_points(multipolygon_with_holes)
    assert count_values_by_type(geometries, LineString) == 24
    assert len(geometries) == 24

def test_geometry_cut_geometrycollection_features_at_points_from_points(geometrycollection):
    geometries = geometry_cut_lines_features_at_points_from_points(geometrycollection)
    assert count_values_by_type(geometries, LineString) == 78
    assert len(geometries) == 78

def test_geometry_get_geometry_coords_from_points(point):
    x, y, xy = geometry_get_geometry_coords(point)
    print(xy)
    assert isinstance(x, float)
    assert isinstance(y, float)
    assert isinstance(xy, tuple)
    assert len(xy) == 3

def test_geometry_get_geometry_coords_from_multipoint(multipoint):
    x, y, xy = geometry_get_geometry_coords(multipoint)
    print(x, y, xy)
    assert isinstance(x, float)
    assert isinstance(y, float)
    assert isinstance(xy, tuple)
    assert len(xy) == 3

def test_geometry_get_geometry_coords_from_linestring(linestring):
    x, y, xy = geometry_get_geometry_coords(linestring)
    assert isinstance(x, list)
    assert len(x) == 2
    assert isinstance(y, list)
    assert len(y) == 2
    assert isinstance(xy, list)
    assert len(xy) == 2


def test_geometry_get_geometry_coords_from_multilinestring(multilinestring):
    x, y, xy = geometry_get_geometry_coords(multilinestring)
    assert isinstance(x, list)
    assert len(x) == 14
    assert isinstance(y, list)
    assert len(y) == 14
    assert isinstance(xy, list)
    assert len(xy) == 14


def test_geometry_get_geometry_coords_from_polygon(polygon):
    x, y, xy = geometry_get_geometry_coords(polygon)
    assert isinstance(x[0][0], list)
    assert isinstance(x[0][0][0], float)
    assert len(x[0][0]) == 5
    assert isinstance(y[0][0], list)
    assert isinstance(x[0][0][0], float)
    assert len(y[0][0]) == 5
    assert isinstance(xy, list)
    assert len(xy[0][0]) == 5
    assert isinstance(xy[0][0][0], tuple)
    assert len(xy[0][0][0]) == 3
    assert isinstance(xy[0][0][0][0], float)


def test_geometry_get_geometry_coords_from_multipolygon(multipolygon):
    x, y, xy = geometry_get_geometry_coords(multipolygon)
    assert isinstance(x, list)
    assert len(x) == 2
    assert isinstance(y, list)
    assert len(y) == 2
    assert isinstance(xy, list)
    assert len(xy) == 2


def test_geometry_get_geometry_coords_from_polygon_with_holes(polygon_with_holes):
    x, y, xy = geometry_get_geometry_coords(polygon_with_holes)
    assert isinstance(x[0][0], list)
    assert len(x[0][0]) == 5
    assert isinstance(x[0][0][0], float)
    assert isinstance(y[0][0], list)
    assert len(y[0][0]) == 5
    assert isinstance(y[0][0][0], float)
    assert isinstance(xy, list)
    assert len(xy[0][0][0]) == 3
    assert isinstance(xy[0][0][0][0], float)


def test_geometry_get_geometry_coords_from_multipolygon_with_holes(multipolygon_with_holes):
    x, y, xy = geometry_get_geometry_coords(multipolygon_with_holes)
    assert isinstance(x[0], list)
    assert len(x[0]) == 1
    assert isinstance(y[0], list)
    assert len(y[0]) == 1
    assert isinstance(xy[0], list)
    assert len(xy[0]) == 1


def test_geometry_get_geometry_coords_from_geometrycollection(geometrycollection):

    with pytest.raises(GeometryTypeError) as exception_info:
        x, y, xy = geometry_get_geometry_coords(geometrycollection)
    assert 'no interest to handle GeometryCollection' in str(exception_info.value)


def test_geometry_holes_computing_point(point):
    try:
        filled, catched = geometry_holes_computing(point)
    except AssertionError:
        pytest.fail("Unexpected MyError ..")
    assert filled is None
    assert isinstance(catched, MultiPolygon)
    assert catched.is_empty


def test_geometry_holes_computing_multipoint(multipoint):
    filled, catched = geometry_holes_computing(multipoint)
    assert filled is None
    assert isinstance(catched, MultiPolygon)
    assert catched.is_empty


def test_geometry_holes_computing_polygon(polygon):
    filled, catched = geometry_holes_computing(polygon)
    assert isinstance(filled, Polygon)
    assert not filled.is_empty
    assert isinstance(catched, MultiPolygon)
    assert catched.is_empty


def test_geometry_holes_computing_polygon_with_holes(polygon_with_holes):
    filled, catched = geometry_holes_computing(polygon_with_holes)
    assert isinstance(filled, Polygon)
    assert not filled.is_empty
    assert isinstance(catched, MultiPolygon)
    assert not catched.is_empty


def test_geometry_holes_computing_multipolygon(multipolygon):
    filled, catched = geometry_holes_computing(multipolygon)
    assert isinstance(filled, MultiPolygon)
    assert not filled.is_empty
    assert isinstance(catched, MultiPolygon)
    assert catched.is_empty


def test_geometry_holes_computing_multipolygon_with_holes(multipolygon_with_holes):
    filled, catched = geometry_holes_computing(multipolygon_with_holes)
    assert isinstance(filled, MultiPolygon)
    assert not filled.is_empty
    assert isinstance(catched, MultiPolygon)
    assert not catched.is_empty


def test_geometry_holes_computing_geometrycollection(geometrycollection):
    filled, catched = geometry_holes_computing(geometrycollection)
    assert isinstance(filled, GeometryCollection)
    assert not filled.is_empty
    assert isinstance(catched, MultiPolygon)
    assert not catched.is_empty