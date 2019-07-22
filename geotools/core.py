"""

GeoTools Core

"""

from .helpers.shapely_addons import ShapelyAddons
from .helpers.reprojection_addons import ReprojectionAddons
from .helpers.db_addons import DataBaseAddons

class GeoTools(
    ShapelyAddons,
    ReprojectionAddons,
    DataBaseAddons
):

    __version__ = '0.2'

    def __init__(self):
        """
        Main Constructor

        """
        super().__init__()




