import time, os
from . import create_logger

try:
    os.mkdir('logs')
except Exception as e:
    pass
try:
    os.mkdir('logs/server')
except:
    pass
try:
    folder = 'logs/server/{}'.format(time.strftime("%Y%m%d-%H%M%S"))
    os.mkdir(folder)

    general_logger       = create_logger(folder, 'server', 'log')
    measurement_logger   = create_logger(folder, 'server_analysis', 'csv')

except Exception as e:
    print('Error with Server Logger: ', e)
