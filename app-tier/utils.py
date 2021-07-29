import logging
import os
from time import sleep

import settings as s


def init_logger(name):
    logger = logging.getLogger(name)
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(
        filename='app_tier.log',
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    return logger


def delete_file(file_path):
    print(f'Deleting output beats file {file_path} after 10s')
    sleep(10)

    for ext in s.shapefile_components:
        if os.path.exists(file_path + ext):
            os.remove(file_path + ext)

    if os.path.exists(file_path + '.zip'):
        os.remove(file_path + '.zip')
