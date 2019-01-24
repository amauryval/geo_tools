"""

GeoTools Core

"""

from .helpers.shapely_addons import ShapelyAddons

class GeoTools(ShapelyAddons):

    __version__ = 'alpha0.1'

    def __init__(self,):
        """
        Main Constructor

        """
        super().__init__()



