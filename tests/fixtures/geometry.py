import pytest

from shapely.wkt import loads as wkt_loads

from shapely.geometry import MultiPoint
from shapely.geometry import MultiLineString
from shapely.geometry import MultiPolygon
from shapely.geometry import GeometryCollection


# raw_data
wkt_point_a = 'Point (30 10 5)'
wkt_point_b = 'Point(4 10 3)'

wkt_linestring_a = 'LineString (-0.072 0.85 0, -0.08 0.22 0)'
wkt_linestring_b = 'LineString (-0.63 0.23 0, -0.08 0.22 0)'
wkt_linestring_c = 'LineString (-0.08 0.22 0, 0.49 0.23 0)'
wkt_linestring_d = 'LineString (0.65 0.47 0, 0.49 0.23 0)'
wkt_linestring_e = 'LineString (-0.29 -0.07 0, -0.08 0.22 0)'
wkt_linestring_f = 'LineString (-0.37 -0.31 0, -0.29 -0.07 0)'
wkt_linestring_g = 'LineString (0.23 -0.13 0, -0.29 -0.07 0)'
wkt_linestring_not_simple = 'LineString (30 10, 10 30, 30 40)'

wkt_polygon_simple_a = 'Polygon ((10 10 1, 110 10 2, 110 110 1, 10 110 1, 10 10 1))'
wkt_polygon_simple_b = 'Polygon ((128 11 1, 228 11 2, 228 111 1, 128 111 1, 128 11 1))'
wkt_polygon_with_holes = 'Polygon ((20 130 1, 120 130 2, 120 230 6, 20 230 5, 20 130 1),(30 140 5, 30 150 5, 40 150 5, 40 140 5, 30 140 5),(50 140 5, 50 150 5, 60 150 5, 60 140 5, 50 140 5))'
wkt_multipolygon_simple = 'MultiPolygon (((14 -101 1, 114 -101 2, 114 -1 1, 14 -1 1, 14 -101 1)))'
wkt_multipolygon_with_holes = 'MultiPolygon (((138 134 1, 238 134 2, 238 234 6, 138 234 5, 138 134 1),(148 144 5, 148 154 5, 158 154 5, 158 144 5, 148 144 5),(168 144 5, 168 154 5, 178 154 5, 178 144 5, 168 144 5)))'


@pytest.fixture
def point():
    return wkt_loads(wkt_point_a)


@pytest.fixture
def multipoint():
    return MultiPoint(points=[
        wkt_loads(wkt_point_a),
        wkt_loads(wkt_point_b)
    ])


@pytest.fixture
def linestring():
    return wkt_loads(wkt_linestring_a)


@pytest.fixture
def linestring_not_simple():
    return wkt_loads(wkt_linestring_not_simple)


@pytest.fixture
def multilinestring():
    # TODO not a really a good multilinestring, change it
    return MultiLineString(lines=[
        wkt_loads(wkt_linestring_a),
        wkt_loads(wkt_linestring_b),
        wkt_loads(wkt_linestring_c),
        wkt_loads(wkt_linestring_d),
        wkt_loads(wkt_linestring_e),
        wkt_loads(wkt_linestring_f),
        wkt_loads(wkt_linestring_g)
    ])


@pytest.fixture
def polygon():
    return wkt_loads(wkt_polygon_simple_a)


@pytest.fixture
def polygon_with_holes():
    return wkt_loads(wkt_polygon_with_holes)


@pytest.fixture
def multipolygon():
    return MultiPolygon(polygons=[
        wkt_loads(wkt_polygon_simple_a),
        wkt_loads(wkt_polygon_simple_b)
    ])


@pytest.fixture
def multipolygon_duplicate():
    return MultiPolygon(polygons=[
        wkt_loads(wkt_polygon_simple_a),
        wkt_loads(wkt_polygon_simple_a)
    ])


@pytest.fixture
def multipolygon_with_holes():
    return wkt_loads(wkt_multipolygon_with_holes)


@pytest.fixture
def geometrycollection():
    return GeometryCollection(geoms=[
        wkt_loads(wkt_point_a),
        MultiPoint(points=[
            wkt_loads(wkt_point_a),
            wkt_loads(wkt_point_b)
        ]),
        wkt_loads(wkt_linestring_a),
        MultiLineString(lines=[
            wkt_loads(wkt_linestring_a),
            wkt_loads(wkt_linestring_b)
        ]),
        wkt_loads(wkt_polygon_simple_a),
        wkt_loads(wkt_polygon_with_holes),
        MultiPolygon(polygons=[
            wkt_loads(wkt_polygon_simple_a),
            wkt_loads(wkt_polygon_simple_b)
        ]),
        wkt_loads(wkt_multipolygon_with_holes)
    ])
