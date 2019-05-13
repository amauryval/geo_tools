"""

shapely_addons.py

"""

from shapely.geometry import GeometryCollection
from shapely.geometry import LineString
from shapely.geometry import LinearRing
from shapely.geometry import MultiLineString
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from shapely.geometry import Point
from shapely.geometry import MultiPoint
from shapely.geometry.polygon import InteriorRingSequence

from shapely.wkb import loads as wkb_loads

from collections import Counter

from collections import OrderedDict


class GeometryTypeError(Exception):
    pass


class ShapelyAddons:
    """
    Class : ShapelyAddons
    """

    @staticmethod
    def __check_empty_geom(geometry):
        if geometry.is_empty:
            return geometry

    @staticmethod
    def __assert_all_geometry_type(geometry):
        assert isinstance(
            geometry,
            (Point, LineString, LinearRing, Polygon, MultiPoint, MultiLineString, MultiPolygon, GeometryCollection, InteriorRingSequence)
        ), 'Geometry not recognized: got %s' % type(geometry)

    @staticmethod
    def __assert_multipart_geometry(geometry):
        assert isinstance(
            geometry,
            (MultiPoint, MultiLineString, MultiPolygon, GeometryCollection)
        ), 'Need a Multi* geometry, got %s' % geometry.geom_type

    def remove_z_geom(self, geometry):
        """
        remove_z_geom

        :type geometry: shapely.geometry.*
        :rtype: shapely.geometry.*
        """

        self.__assert_all_geometry_type(geometry)

        if geometry.is_empty:
            return geometry

        if isinstance(geometry, Polygon):
            exterior = geometry.exterior
            new_exterior = self.remove_z_geom(exterior)
            interiors = geometry.interiors
            new_interiors = []
            for interior in interiors:
                new_interiors.append(self.remove_z_geom(interior))

            return Polygon(new_exterior, new_interiors)

        elif isinstance(geometry, (LineString, LinearRing, Point)):
            return type(geometry)([xy[0:2] for xy in list(geometry.coords)])

        elif isinstance(geometry, (MultiPoint, MultiLineString, MultiPolygon, GeometryCollection)):
            geometries = list(geometry.geoms)
            new_geometries = []
            for geom in geometries:
                new_geometries.append(self.remove_z_geom(geom))

            return type(geometry)(new_geometries)

    def get_intersection_nodes(self, lines, mode='crossroads'):
        #TODO CHANGE INPUT : should not be MultiLineString but a list of LineString
        """
        get_intersection_nodes
        compute nodes from MultiLineString:
            - crossroads : lines intersections (>= 3 nodes)
            - dead_ends : line without intersections (= 1 node)
            - section : continuous lines (= 2 nodes)

        :type lines: shapely.geometry.MultiLineString
        :type mode: str, default: crossroads. ['dead_ends', 'sections']
        :rtype: shapely.geometry.MultiPoint
        """

        def computational_func(mode):
            if mode == 'crossroads':
                return [wkb_loads(geom) for geom, count in counter.most_common() if count >= 3]
            elif mode == 'dead_ends':
                return [wkb_loads(geom) for geom, count in counter.most_common() if count == 1]
            elif mode == 'sections':
                return [wkb_loads(geom) for geom, count in counter.most_common() if count == 2]

        assert isinstance(lines, MultiLineString), 'Need MultiLineString geometry, got %s!' % lines.geom_type

        geometries = lines.geoms
        counter = Counter([Point(f).wkb for line in geometries for f in line.coords])

        return MultiPoint(computational_func(mode))

    def convert_geometry_to_simple_linestrings(self, geometry):
        """
        convert_geometry_to_simple_linestrings
        convert elements found in MultiLineString to a new MultiLineString containing
        LineStrings with 2 coordinates

        :type geometry: shapely.geometry.*
        :rtype: [shapely.geometry.Linestring]
        """

        self.__assert_all_geometry_type(geometry)

        new_geometries = []


        if isinstance(geometry, (LineString, LinearRing)):
            new_geometries = [LineString(pair) for pair in zip(geometry.coords[:-1], geometry.coords[1:])]

        elif isinstance(geometry, Polygon):
            # new_geometries = []
            new_geometries.extend(
                self.convert_geometry_to_simple_linestrings(geometry.exterior).geoms
            )

            for interior in geometry.interiors:
                new_geometries.extend(self.convert_geometry_to_simple_linestrings(interior).geoms)

        elif isinstance(geometry, (MultiLineString, MultiPolygon, GeometryCollection)):
            geometries = geometry.geoms
            for geom in geometries:
                line = self.convert_geometry_to_simple_linestrings(geom).geoms
                new_geometries.extend(line)

        elif isinstance(geometry, (Point, MultiPoint)):
            # geom not processing
            new_geometries = None

        return MultiLineString(new_geometries)


    def convert_geometry_to_points(self, geometry, drop_duplicates=False):
        """
        geometry_to_points

        :type geometry: shapely.geometry.*
        :rtype: [shapely.geometry.Point]
        """

        self.__assert_all_geometry_type(geometry)

        new_geometry = []

        if isinstance(geometry, Point):
            new_geometry.append(geometry)

        if isinstance(geometry, Polygon):
            # prepare polygon objects
            new_geometry.extend(
                self.convert_geometry_to_points(geometry.exterior, drop_duplicates).geoms
            )
            for interior in geometry.interiors:
                new_geometry.extend(self.convert_geometry_to_points(interior, drop_duplicates).geoms)

        elif isinstance(geometry, (LinearRing, LineString)):
            for coord in geometry.coords:
                point = self.convert_geometry_to_points(Point(coord), drop_duplicates).geoms
                new_geometry.extend(point)

        elif isinstance(geometry, (MultiPoint, MultiLineString, MultiPolygon, GeometryCollection)):
            for geom in geometry.geoms:
                points = self.convert_geometry_to_points(geom, drop_duplicates).geoms
                new_geometry.extend(points)

        new_geometry = MultiPoint(new_geometry)

        if drop_duplicates:
            new_geometry = self.drop_duplicates_geometry(new_geometry)

        return new_geometry

    def drop_duplicates_geometry(self, geometry):

        self.__assert_multipart_geometry(geometry)

        unique_points = list(set([new.wkb for new in geometry.geoms]))
        new_geometry = type(geometry)([wkb_loads(coords) for coords in unique_points])

        return new_geometry

    def create_point_along_line_features(self, geometry, ratio=0.5):
        """
        create_point_along_line_features

        :type geometry: shapely.geometry.*
        :type ratio: float
        :return: [shapely.geometry.point]
        """

        self.__assert_all_geometry_type(geometry)

        new_geometries = []

        if isinstance(geometry, (LineString, LinearRing)):
            new_geometries = [geometry.interpolate(ratio, normalized=True)]

        elif isinstance(geometry, MultiLineString):
            geometries = self.convert_geometry_to_simple_linestrings(geometry).geoms
            new_geometries = []
            for geometry in geometries:
                points = self.create_point_along_line_features(geometry).geoms
                new_geometries.extend(points)

        elif isinstance(geometry, (Polygon, MultiLineString, MultiPolygon, GeometryCollection)):
            geometries = self.convert_geometry_to_simple_linestrings(geometry).geoms
            for geom in geometries:
                points = self.create_point_along_line_features(geom).geoms
                new_geometries.extend(points)

        return MultiPoint(new_geometries)

    def cut_line_features_at_points(self, geometry, ratio=0.5, points=None):
        """
        cut_line_features_at_points

        :type geometry: shapely.geometry.*
        :type ratio: float, default: 0.5
        :type points: [shapely.geometry.Point], default None
        :return: [shapely.geometry.LineString]
        """
        self.__assert_all_geometry_type(geometry)

        new_geometries = []

        if isinstance(geometry, (LineString, LinearRing)):

            new_geometries = list(geometry.coords)
            if ratio is not None:
                points_coords = [geometry.interpolate(ratio, normalized=True).xy]
                new_geometries[1:1] = points_coords

            elif points is not None:

                start_point = Point(new_geometries[0])
                points_on_line_mapping = {
                    point.coords[0]: start_point.distance(point)
                    for point in points
                    if start_point.distance(point) > 0 and start_point.distance(point) < geometry.length and geometry.envelope.intersects(point.envelope)
                }

                if len(points_on_line_mapping) > 0:
                    points_on_line_mapping_sorted = OrderedDict(sorted(points_on_line_mapping.items(), key=lambda x: x[1]))
                    points_coords = [point for point in points_on_line_mapping_sorted]
                    new_geometries[1:1] = points_coords
                    new_geometries = [LineString(pair) for pair in zip(new_geometries[:-1], new_geometries[1:])]
                else:
                    new_geometries = [geometry]

        elif isinstance(geometry, MultiLineString):
            geometries = geometry.geoms
            for geometry in geometries:
                lines = list(self.cut_line_features_at_points(geometry, ratio, points).geoms)
                new_geometries.extend(lines)

        elif isinstance(geometry, (Point, MultiPoint)):
            new_geometries = None

        else:
            geom_lines = self.convert_geometry_to_simple_linestrings(geometry).geoms
            for geom in geom_lines:
                lines = self.cut_line_features_at_points(geom, ratio, points).geoms
                new_geometries.extend(lines)

        return MultiLineString(new_geometries)

    def geometry_2_bokeh_format(self, geometry, coord_name='xy', input_is_a_point=True):
        """
        geometry_2_bokeh_format
        Used for bokeh library

        :type geometry: shapely.geometry.*
        :type coord_name: str, default: xy (x or y)
        :return: float or list of tuple
        """

        self.__assert_all_geometry_type(geometry)

        coord_values = []

        if isinstance(geometry, Point):
            if coord_name != 'xy':
                coord_values = getattr(geometry, coord_name)
            else:
                coord_values = next(iter(geometry.coords))

        elif isinstance(geometry, Polygon):
            exterior = [self.geometry_2_bokeh_format(geometry.exterior, coord_name)]
            interiors = self.geometry_2_bokeh_format(geometry.interiors, coord_name)
            coord_values = [
                exterior,
                interiors
            ]
            if len(interiors) == 0:
                coord_values = [
                    exterior
                ]

        elif isinstance(geometry, (LinearRing, LineString)):
            coord_values = [
                self.geometry_2_bokeh_format(Point(feat), coord_name)
                for feat in geometry.coords
            ]

        if isinstance(geometry, (MultiPoint, MultiPolygon, MultiLineString)):
            for feat in geometry.geoms:
                if isinstance(feat, Point):
                    coord_values = self.geometry_2_bokeh_format(feat, coord_name)
                else:
                    coord_values.extend(self.geometry_2_bokeh_format(feat, coord_name))

        if isinstance(geometry, InteriorRingSequence):
            #compute holes
            coord_values.extend([
                self.geometry_2_bokeh_format(feat, coord_name)
                for feat in geometry
            ])

        if isinstance(geometry, GeometryCollection):
            raise GeometryTypeError('no interest to handle GeometryCollection')

        return coord_values

    def fill_holes(self, geometry, hole_area_to_fill):
        """
        rm_area

        :type geometry: shapely.geometry.polygon or shapely.geometry.multipolygon
        :type hole_area_to_fill: float
        :return:
        """
        self.__assert_all_geometry_type(geometry)

        new_geometries = None

        if isinstance(geometry, (MultiPolygon, GeometryCollection)):
            new_geometries = [
                self.fill_holes(geom, hole_area_to_fill)
                for geom in geometry.geoms
            ]
            new_geometries = type(geometry)([
                geom
                for geom in new_geometries
                if geom is not None
            ])

        elif isinstance(geometry, Polygon):
            initial_interiors_count = len(list(geometry.interiors))
            interiors_left = [
                geom
                for geom in list(geometry.interiors)
                if Polygon(geom).area > hole_area_to_fill
            ]
            interiors_count_deleted = initial_interiors_count - len(interiors_left)

            print('%s holes will be removed.' % interiors_count_deleted)
            new_geometries = Polygon(
                geometry.exterior,
                interiors_left
            )

        return new_geometries

    def get_holes(self, geometry, hole_area_to_fill):
        """
        get_holes

        :type geometry: shapely.geometry.polygon
        :type hole_area_to_fill: float
        :return:
        """
        self.__assert_all_geometry_type(geometry)

        new_geometries = []

        if isinstance(geometry, (MultiPolygon, GeometryCollection)):
            new_geometries = [
                interior
                for geom in geometry
                for interior in self.get_holes(geom, hole_area_to_fill)
                if geom.geom_type == 'Polygon'
            ]

        elif isinstance(geometry, Polygon):
            new_geometries = [
                Polygon(geom)
                for geom in list(geometry.interiors)
                if Polygon(geom).area <= hole_area_to_fill
            ]

        return MultiPolygon(new_geometries)


    def _buffer_side_on_line(self, geometry, distance, side):
        """

        :type geometry: shapely.geometry.LineString or MultiLineString
        :type distance: float
        :param side: str (enum: left or right)
        :type: shapely.geometry.Polygon or MultiPolygon
        """

        polygon = []
        if isinstance(geometry, LineString):
            parallel_line = geometry.parallel_offset(distance, side).coords
            source_line = geometry.coords

            if side == 'left':
                parallel_line = parallel_line[::-1]

            polygon = Polygon([*source_line, *parallel_line, source_line[0]])

        elif isinstance(geometry, MultiLineString):
            polygon = MultiPolygon([
                self._buffer_side_on_line(geom, distance, side)
                for geom in geometry.geoms
            ])

        return polygon
