import logging
import time
filename = '{}'.format(time.strftime("%Y%m%d-%H%M%S"))

general_logger = logging.getLogger(name='GeneralLog')
measurement_logger = logging.getLogger(name='MeasurementLog')

c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('logs/client/')
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)