import logging
import os
import boto3
import shutil
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


def delete_file(file_path, sleep_time=10):
    logger = init_logger(__name__)

    logger.info(f'Deleting shapefile residue {file_path} after {sleep_time}s')
    sleep(sleep_time)

    for ext in s.shapefile_components:
        if os.path.exists(file_path + ext):
            os.remove(file_path + ext)

    if os.path.exists(file_path + '.zip'):
        os.remove(file_path + '.zip')


def download_file_from_s3(bucket_name, object_name):
    s3_resource = boto3.resource('s3')
    s3_resource.Bucket(bucket_name).download_file(f'{s.s3_polygon_wise_count_shapefile}/{object_name}',
                                                  f'data/input/{object_name}')
    shutil.unpack_archive(f'data/input/{object_name}', f'data/input/')
