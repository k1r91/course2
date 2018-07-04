import logging


def get_logger(name, filename):
    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s -%(threadName)s - %(message)s ')
    fh = logging.FileHandler(filename, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)
    return logger
