
import os
import sys
import datetime
import logging


class LoggerAddons:
    """
    Class : LoggerAddons
    """

    _formatter = logging.Formatter(
        '%(asctime)s - %(name)-13s - %(levelname)-8s : %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    _log_date_file_format = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")

    _percent_step = 5

    def __init__(self, logger_name=None, logger_level='info', logger_dir=None, raise_error=False):
        """
        Main Constructor

        """
        self._logger_name = logger_name if logger_name else self.__class__.__name__
        print(logger_dir, self.__class__.__name__)
        self.logger = self._create_logger(
            logger_level,
            f'/{logger_dir}/{self.__class__.__name__}' if logger_dir is not None else None
        )
        self.raise_error = raise_error
        self.progress_value = self._percent_step
        self.step_log_progress = self._percent_step

    def _create_logger(self, logger_level, logger_dir):
        """
        create a logger

        :param logger_level: str
        :param logger_file: str
        :return:
        """

        levels = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }


        logger_init = logging.getLogger(self._logger_name)
        logger_init.setLevel(levels[logger_level] if logger_level in levels else logging.DEBUG)

        if not logger_init.handlers:
            logger_init.setLevel(levels[logger_level] if logger_level in levels else logging.DEBUG)

            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(levels[logger_level] if logger_level in levels else logging.DEBUG)
            handler.setFormatter(self._formatter)
            logger_init.addHandler(handler)

            if logger_dir is not None:
                try:
                    os.stat('logs')
                except:
                    os.mkdir('logs')
                try:
                    os.stat(f'logs{os.path.dirname(logger_dir)}')
                except:
                    os.mkdir(f'logs{os.path.dirname(logger_dir)}')

                handler_file = logging.FileHandler(f'logs{logger_dir}_{self._log_date_file_format}.txt')
                handler_file.setLevel(levels[logger_level] if logger_level in levels else logging.DEBUG)
                handler_file.setFormatter(self._formatter)
                logger_init.addHandler(handler_file)

        return logger_init

    ############################################################################
    # logger methods
    ############################################################################

    def info(self, message):
        return self.logger.info(f'{message.upper()}')

    def warning(self, message):
        return self.logger.warning(f'{message.upper()}')