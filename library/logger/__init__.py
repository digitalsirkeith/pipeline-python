import logging, time, os

logging.getLogger().setLevel(logging.WARNING)

def create_logger(folder, name, file_type):
    filename='{}/{}.{}'.format(folder, name, file_type)
    logger = logging.getLogger(name=name)
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.WARNING)

    if file_type == 'csv':
        formatter = logging.Formatter('%(message)s')
    else:
        formatter = logging.Formatter('[%(asctime)s] (%(process)s) %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger