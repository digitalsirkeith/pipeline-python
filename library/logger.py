import logging, time, os

def create_logger(folder, name, file_type):
    logger = logging.getLogger(name=name)
    handler = logging.FileHandler('{}/{}.{}'.format(folder, name, file_type))
    handler.setLevel(logging.INFO)

    if file_type == 'csv':
        formatter = logging.Formatter('%(message)s')
    else:
        formatter = logging.Formatter('[%(asctime)s] (%(name)s) %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(logger)

    return logger

try:
    client_folder = 'logs/client/{}'.format(time.strftime("%Y%m%d-%H%M%S"))
    server_folder = 'logs/server/{}'.format(time.strftime("%Y%m%d-%H%M%S"))
    os.mkdir(client_folder)
    os.mkdir(server_folder)

    client_general_logger       = create_logger(client_folder, 'ClientGeneralLog', 'log')
    client_measurement_logger   = create_logger(client_folder, 'client_analysis', 'csv')
    server_general_logger       = create_logger(client_folder, 'ServerGeneralLog', 'log')
    server_measurement_logger   = create_logger(client_folder, 'server_analysis', 'csv')

except Exception as e:
    print('Error with Logger: ', e)
