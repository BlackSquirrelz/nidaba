import logging
import os
import time
import datetime


class Logger:
    _logger = None

    def __new__(cls, *args, **kwargs):
        if cls._logger is None:
            print("Logger new")
            cls._logger = super().__new__(cls, *args, **kwargs)
            cls._logger = logging.getLogger("crumbs")
            cls._logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s')

            now = datetime.datetime.now()
            dirname = "./log"

            if not os.path.isdir(dirname):
                os.mkdir(dirname)
            file_handler = logging.FileHandler(
                dirname + "/log_" + now.strftime("%Y-%m-%d") + ".log")

            stream_handler = logging.StreamHandler()

            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)

            cls._logger.addHandler(file_handler)
            cls._logger.addHandler(stream_handler)

        return cls._logger

"""# Get some logging setup
    # TODO: Define further logging levels
    if args.verbose:
        logging_level = logging.INFO
    else:
        logging_level = logging.WARNING

    log_name = str(cur_date) + "_basic.log"
    logging.basicConfig(filename=log_name, level=logging_level)

    logging.info("It works.")
    logging.info(f"Loaded Modules {modules}")"""
