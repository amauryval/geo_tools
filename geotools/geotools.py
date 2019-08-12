"""

GeoTools Core

"""

from .helpers.db_addons import DataBaseAddons
from .helpers.shapely_addons import ShapelyAddons
from .helpers.reprojection_addons import ReprojectionAddons


class GeoTools(
    ShapelyAddons,
    ReprojectionAddons,
    DataBaseAddons,
):
    __version__ = '0.2'

    def __init__(self, logger_dir=None, *args, **kwargs):
        """
        Main Constructor

        :param logger_dir: to create directory log output
        :type logger_dir: str
        """
        super().__init__(logger_dir=logger_dir, *args, **kwargs)
