from .logger_addons import LoggerAddons

from sqlalchemy import MetaData


class GeoToolsCore(LoggerAddons):

    def __init__(self):
        super().__init__()
        self.info_title(self.__class__.__name__)

    #############################
    #     global DB method      #
    def get_metadata(self, engine, schema):

        return MetaData(
            bind=engine,
            schema=schema
        )