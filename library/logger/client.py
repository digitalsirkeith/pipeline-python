import time, os
from . import create_logger

try:
    os.mkdir('logs')
except Exception as e:
    pass
try:
    os.mkdir('logs/client')
except:
    pass
try:
    folder = 'logs/client/{}'.format(time.strftime("%Y%m%d-%H%M%S"))
    os.mkdir(folder)

    general_logger       = create_logger(folder, 'client', 'log')
    measurement_logger   = create_logger(folder, 'client_analysis', 'csv')

except Exception as e:
    print('Error with Client Logger: ', e)
