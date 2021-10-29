# AWS Services Installation Guide
Smartbeats application is dependent upon a shared object store and a database that both web and app-tier can access. We are using **Amazon S3** as object storage and **Amazon Aurora** as database. Using **Aurora** is our decision choice. Any other shared database (b/w web and app tiers) would also work perfectly with Smartbeats.

## Amazon S3
1. Smartbeats require one main bucket and four sub-directories inside that bucket.
2. Create the Amazon S3 buckets and set proper permissions using the [S3 documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)
3. Create the buckets and sub-directories using the example bucket layout below:
```
smartbeats-main-bucket
├── beat_shapefiles_dir
├── city_crime_datasets_dir
├── city_shapefiles_dir
└── polygon_wise_count_shapefiles_dir
```
4. Update the bucket configuration in web-tier `settings.py` file.
> You can add your bucket configuration as environment variables (inside `.bashrc`) and load them as below in the `settings.py` config file
```
AWS_STORAGE_BUCKET_NAME = os.environ['smartbeats-main-bucket']
S3_BEAT_SHAPEFILES_DIR = os.environ['beat_shapefiles_dir']
S3_CITY_CRIME_DS_DIR = os.environ['city_crime_datasets_dir']
S3_CITY_SHAPEFILES_DIR = os.environ['city_shapefiles_dir']
S3_POLYGON_WISE_COUNT_SHAPEFILE_DIR = os.environ['polygon_wise_count_shapefiles_dir']
```

5. Update the bucket configuration in app-tier `settings.py` file.
> You can add your bucket configuration as environment variables (inside `.bashrc`) and load them as below in the `settings.py` config file
```
output_s3_bucket_name = os.environ['smartbeats-main-bucket']
s3_beats_dir_name = os.environ['beat_shapefiles_dir']
s3_polygon_wise_count_shapefile = os.environ['polygon_wise_count_shapefiles_dir']
```

## Amazon Aurora
1. Create the Amazon Aurora Database and set proper permissions using the [Aurora documentation](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.CreateInstance.html).
2. That's it!! The user doesn't need to manually create any tables. [Installation of web-tier](https://github.com/ASUCICREPO/smart-beats/blob/master/web-tier/README.md) will create all necessary tables automatically.