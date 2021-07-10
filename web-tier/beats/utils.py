import logging
import boto3
import geopandas as gpd
import io

s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')
AWS_STORAGE_BUCKET_NAME = 'smart-beats-cic'


# Logging
def init_logger(name):
    logger = logging.getLogger(name)
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(
        filename='web_tier.log',
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    return logger


def get_shapefile_gdf(city_obj):
    gdf = gpd.read_file(city_obj.city_shapefile.url)
    return gdf
