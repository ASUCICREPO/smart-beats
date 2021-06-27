from storages.backends.s3boto3 import S3Boto3Storage


class ShapefileStorage(S3Boto3Storage):
    bucket_name = 'city-shapefiles'


class CrimeDataStorage(S3Boto3Storage):
    bucket_name = 'city-crime-data'


class TestDataStorage(S3Boto3Storage):
    bucket_name = 'dryrun-xplod'
