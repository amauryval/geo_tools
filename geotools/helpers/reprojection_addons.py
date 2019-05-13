

class ReprojectionAddons:
    """
    Class : ReprojectionAddons
    """

    def is_from_and_to_epsg_are_equals(self, from_epsg, to_epsg):

        if from_epsg == to_epsg:
            print(f'from_epsg{from_epsg} and to_epsg{to_epsg} are equals: reprojection aborted!')
            return True

        return False

    def pyproj_reprojection(self, geometry, from_epsg, to_epsg):
        """
        pyproj_reprojection

        :type geometry: shapely.geometry.*
        :type from_epsg: int
        :type to_epsg: int
        :rtype: shapely.geometry.*
        """

        import pyproj
        from shapely.ops import transform
        from functools import partial

        if not self.is_from_and_to_epsg_are_equals(from_epsg, to_epsg):
            geometry = transform(
                partial(
                    pyproj.transform,
                    pyproj.Proj(init=f'epsg:{from_epsg}'),
                    pyproj.Proj(init=f'epsg:{to_epsg}')
                ),
                geometry
            )

        return geometry


    def ogr_reprojection(self, geometry, from_epsg, to_epsg):
        """
        ogr_reprojection

        :type geometry: shapely.geometry.*
        :type from_epsg: int
        :type to_epsg: int
        :rtype: shapely.geometry.*
        """

        from osgeo import ogr
        from osgeo import osr
        from shapely.wkt import loads

        if not self.is_from_and_to_epsg_are_equals(from_epsg, to_epsg):
            source_epsg = osr.SpatialReference()
            source_epsg.ImportFromEPSG(from_epsg)

            target_epsg = osr.SpatialReference()
            target_epsg.ImportFromEPSG(to_epsg)

            transform = osr.CoordinateTransformation(source_epsg, target_epsg)
            ogr_geom = ogr.CreateGeometryFromWkt(
                geometry.wkt
            )
            ogr_geom.Transform(transform)
            geometry = loads(ogr_geom.ExportToWkt())

        return geometry