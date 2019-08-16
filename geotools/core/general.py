from .logger_addons import LoggerAddons

class GeoToolsCore(LoggerAddons):

    def __init__(self):
        super().__init__()
        self.info_title(self.__class__.__name__)
