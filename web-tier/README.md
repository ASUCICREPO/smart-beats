# Web-tier Installation Guide
> Web-tier is developed using Python + [Django](https://www.djangoproject.com/) Framework

## Prerequisites
* A Unix-like (macOS, Linux, BSD) or Windows operating system with a command line terminal and `git` installed
* Python-3 should be installed
* Existing Database tables and S3 buckets in AWS. Refer [AWS Services guide](https://github.com/ASUCICREPO/smart-beats/blob/master/AWS_Services.md).

## Basic Installation
1. Smartbeats repository contains the codebase of both web and app tiers
   
2. Pull the github repository: [Smartbeats](https://github.com/ASUCICREPO/smart-beats)
   
3. Go to web-tier directory.
```
cd smart-beats/web-tier/
```

4. Create Python virtual environment
```
python -m venv venv/
source venv/bin/activate
```

5. Install dependencies from `requirements.txt`
```
pip install -r requirements.txt
```

6. Update configuration file `./smartbeats/settings.py`. Refer [AWS Services guide](https://github.com/ASUCICREPO/smart-beats/blob/master/AWS_Services.md) for AWS configurations. 

> You can add your AWS credentials as environment variables (inside `.bashrc`) and load them using `os.environ['property']` in the config file 

The User specified configuration section is in the following format:
```python
# ========================= User specified application settings: START ========================= #
# City table
CITY = 'Glendale'
STATE = 'Arizona'
COUNTRY = 'USA'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ['AURORA_DB_NAME'],
        'USER': os.environ['AURORA_USERNAME'],
        'PASSWORD': os.environ['AURORA_PASSWORD'],
        'HOST': os.environ['AURORA_HOSTNAME'],
        'PORT': os.environ['AURORA_PORT'],
    }
}

# AWS credentials
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_REGION_NAME = 'us-east-1'
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_FILE_OVERWRITE = False

S3_BEAT_SHAPEFILES_DIR = os.environ['S3_BEAT_SHAPEFILES_DIR']
S3_CITY_CRIME_DS_DIR = os.environ['S3_CITY_CRIME_DS_DIR']
S3_CITY_SHAPEFILES_DIR = os.environ['S3_CITY_SHAPEFILES_DIR']
S3_POLYGON_WISE_COUNT_SHAPEFILE_DIR = os.environ['S3_POLYGON_WISE_COUNT_SHAPEFILE_DIR']

# Sample Priority choices
PRIORITY_CHOICES = ((1, 1),
                    (2, 2),
                    (3, 3),
                    (4, 4),
                    (5, 5),
                    (6, 6),
                    (7, 7),
                    (9, 9),
                    )

# Sample Disposition choices
DISPOSITION_CHOICES = ((1, '1 - Field Interview'),
                       (2, '2 - False Alarm'),
                       (3, '3 - Unable to locate'),
                       (5, '5 - Assist Fire Department'),
                       (6, '6 - Report'),
                       (9, '9 - Contact made'),
                       )

# Write your Application server URL here
APP_SERVER_URL = "http://ec2-xxxxxxxxxxxxxx.amazonaws.com"
# ========================= User specified application settings: END ========================= #
```

7. Create database tables
```
python manage.py makemigrations
python manage.py migrate
```

8. Run the server
```
python manage.py runserver
```

> Note: The above installation steps create a Django Development server which hosts the web-tier of Smartbeats. Django server is for development purpose only. For production environment, use a robust server like deploying on [Nginx](https://www.nginx.com/) + [Gunicorn](https://gunicorn.org/).

