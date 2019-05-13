"""

GeoTools Core

"""

from .helpers.shapely_addons import ShapelyAddons
from .helpers.reprojection_addons import ReprojectionAddons

class GeoTools(
    ShapelyAddons,
    ReprojectionAddons
):

    __version__ = '0.2'

    def __init__(self):
        """
        Main Constructor

        """
        super().__init__()




