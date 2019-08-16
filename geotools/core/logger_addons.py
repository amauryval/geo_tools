
import os
import sys
import datetime
import logging


class LoggerAddons:
    """
    Class : LoggerAddons
    """
    _log_dir = 'logs'
    _formatter = logging.Formatter(
        '%(asctime)s - %(name)-15s - %(levelname)-8s : %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    _log_date_file_format = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")

    _percent_step = 5

    def __init__(self, parent=None, logger_name=None, logger_level='info', logger_dir=None, raise_error=False):
        """
        Main Constructor

        """
        if not parent:
            self._logger_name = logger_name if logger_name else self.__class__.__name__

            self.logger = self._create_logger(
                logger_level,
                f'/{logger_dir}/{self.__class__.__name__}' if logger_dir is not None else None
            )
            self.raise_error = raise_error
            self.init_log_progress()
        else:
            self.logger_name = parent.logger_name
            self.logger = parent.logger
            self.raise_error = parent.raise_error
            self.progress_value = parent.progress_value
            self.step_log_progress = parent.step_log_progress

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
                log_path = f'{self._log_dir}_{self._log_date_file_format}'
                complete_log_path = f'{log_path}{os.path.dirname(logger_dir)}'

                if not os.path.isdir(complete_log_path):
                    os.makedirs(complete_log_path)

                handler_file = logging.FileHandler(f'{log_path}{logger_dir}.txt')
                handler_file.setLevel(levels[logger_level] if logger_level in levels else logging.DEBUG)
                handler_file.setFormatter(self._formatter)
                logger_init.addHandler(handler_file)

        return logger_init

    def init_log_progress(self, step_percent=5):

        self.progress_value = step_percent
        self.step_log_progress = step_percent

    def log_progress(self, percentage, message="Progress : %s %%"):

        if percentage == 0.0:
            self.logger.info(message, 0)

        elif percentage >= self.progress_value:
            self.logger.info(message, self.progress_value)
            self.progress_value += self.step_log_progress

        elif percentage == 100.0:
            self.logger.info(message, self.progress_value)
            self.logger.info(message % self.progress_value)

    #########################################
    #   Logger methods
    #
    def info(self, message):
        return self.logger.info(f'{message.title()}')

    def warning(self, message):
        return self.logger.warning(f'{message.title()}')

    def info_title(self, message):
        return self.logger.info(f'-== {message.title()} ==-')
    #
    #   Logger methods
    #########################################
