# App-tier Installation Guide
> App-tier is developed using Python + [Flask](https://flask.palletsprojects.com/en/2.0.x/) Framework

## Prerequisites
1. A Windows operating system with a command line terminal and `git` installed
> App-tier is dependent upon ArcGis Pro. For development purpose
2. [ArcGis Pro](https://pro.arcgis.com/en/pro-app/latest/get-started/get-started.htm) installed with [subscription](https://www.esri.com/en-us/arcgis/products/arcgis-pro/buy)
3. Python-3 + Miniconda should be installed


## Basic Installation
1. Smartbeats repository contains the codebase of both web and app tiers
   
2. Open ArcGIS Pro `python` terminal `C:\Users\User-XYZ\AppData\Local\Programs\ArcGIS\Pro\bin\Python\Scripts\proenv.bat`
   
3. Pull the github repository: [Smartbeats](https://github.com/ASUCICREPO/smart-beats)
   
4. Go to app-tier directory
```
cd smart-beats/app-tier/
```

5. Install dependencies from `requirements.txt`
```
pip install -r requirements.txt
```

6. Update configuration file `./settings.py` with S3 bucket names created in [AWS services installation](https://github.com/ASUCICREPO/smart-beats/blob/master/AWS_Services.md) step.

> You can add your AWS credentials as environment variables (inside `.bashrc`) and load them using `os.environ['property']` in the config file 

```
output_s3_bucket_name = os.environ['smartbeats-main-bucket']
s3_beats_dir_name = os.environ['beat_shapefiles_dir']
s3_polygon_wise_count_shapefile = os.environ['polygon_wise_count_shapefiles_dir']

# Specify the path to ArcGIS workspace
ARCGIS_WORKSPACE = 'arcgis-workspace/arcgis-workspace.gdb'
```

7. Run the server
```
python app.py
```

> Note: The above installation steps create a Flask Development server which hosts the web-tier of Smartbeats. Flask server is for development purpose only. For production environment, use a robust server like deploying on [Apache2](https://httpd.apache.org/docs/2.4/platform/windows.html).