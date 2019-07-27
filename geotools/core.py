"""

GeoTools Core

"""

from .helpers.shapely_addons import ShapelyAddons
from .helpers.reprojection_addons import ReprojectionAddons
from .helpers.db_addons import DataBaseAddons
from .helpers.pandas_addons import PandasAddons


class GeoTools(
    ShapelyAddons,
    ReprojectionAddons,
    DataBaseAddons,
    PandasAddons
):

    __version__ = '0.2'

    def __init__(self):
        """
        Main Constructor

        """
        super().__init__()




