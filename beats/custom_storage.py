from storages.backends.s3boto3 import S3Boto3Storage


class ShapefileStorage(S3Boto3Storage):
    bucket_name = 'sb-city-shapefiles'


class CrimeDataStorage(S3Boto3Storage):
    bucket_name = 'sb-city-crime-data'


class TestDataStorage(S3Boto3Storage):
    bucket_name = 'dryrun-test'
