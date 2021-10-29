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

## Amazon Aurora
1. Create the Amazon Aurora Database and set proper permissions using the [Aurora documentation](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.CreateInstance.html).
2. Note down the following database configurations:
```
Name, Username, Passoword, Host, Port
```
3. That's it! The user doesn't need to manually create any tables. [Installation of web-tier](https://github.com/ASUCICREPO/smart-beats/blob/master/web-tier/README.md) will create all necessary tables automatically.