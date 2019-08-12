from abc import ABCMeta
from .logger_addons import LoggerAddons

class GeoToolsCore(LoggerAddons):

    __metaclass__ = ABCMeta

    def __init__(self, logger_dir):
        super().__init__(logger_dir=logger_dir)
