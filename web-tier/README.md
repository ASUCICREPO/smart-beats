# Installation Guide

## Prerequisites
* A Unix-like (macOS, Linux, BSD) or Windows operating system with a command line terminal and `git` installed
* Python-3 should be installed
* Existing Database tables and S3 buckets in AWS. Refer [AWS Services guide](../../smart-beats/AWS_Services.md).

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

6. Update configuration file `./smartbeats/settings.py`. The User specified configuration settings section is in the following format:
```
# ========================= User specified application settings: START ========================= #
.
.
.
.
# ========================= User specified application settings: END ========================= #
```

7. Run the server
```
python manage.py runserver
```

> Note: The above installation steps create a Django Development server which hosts the web-tier of Smartbeats. Django server is for development purpose only. For production environment, use a robust server like deploying on [Nginx](https://www.nginx.com/) + [Gunicorn](https://gunicorn.org/).

