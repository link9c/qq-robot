import os

import logging

from logging.handlers import RotatingFileHandler

log_abspath = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "log")

print("log_path", log_abspath)


def get_logger(log_name, log_path):
    log_path = log_abspath + log_path
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)

    # 写入文件，如果文件超过1M大小时，切割日志文件，仅保留3个文件
    logger_handler = RotatingFileHandler(filename=log_path, maxBytes=32 * 1024 * 1024, backupCount=3, encoding='utf-8')
    logger_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
    return logger
