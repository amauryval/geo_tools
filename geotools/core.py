"""

GeoTools Core

"""

from concurrent.futures import ThreadPoolExecutor

from .helpers.shapely_addons import ShapelyAddons
from .helpers.reprojection_addons import ReprojectionAddons
from .helpers.db_addons import DataBaseAddons
from .helpers.logger_addons import LoggerAddons
from .helpers.perfomance_addons import PerformanceAddons


class GeoTools(
    ShapelyAddons,
    ReprojectionAddons,
    DataBaseAddons,
    LoggerAddons,
    PerformanceAddons
):
    __version__ = '0.2'

    def __init__(self, logger_dir=None, *args, **kwargs):
        """
        Main Constructor

        :param logger_dir: to create directory log output
        :type logger_dir: str
        """
        super(GeoTools, self).__init__(logger_dir=logger_dir, *args, **kwargs)

