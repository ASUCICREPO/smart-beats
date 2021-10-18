# Smartbeats


|Index| Description|
|:----------------|:-----------|
| [Overview](#overview)         |     See the motivation behind this project.    | 
| [Description](#description)         |     Learn more about the problem, implemented solution and challenges faced.    | 
| [Installation Guide](#installation-guide)         |    How to install Smartbeats architecture. |
| [How to Use](#how-to-use)       |     Instructions to use Smartbeats.   |
| [Credits](#credits)      |     Meet the team behind this.     |
| [License](#license)      |     License details.     |



# Overview
The Arizona State University Smart City Cloud Innovation Center Powered by AWS (ASU CIC) recently collaborated with the City of Glendale, Arizona to improve the process for designing and maintaining patrol areas.


Glendale aims to be able to provide a safe and timely response to calls for service. Today this process is done manually and relies on the personal knowledge of those who make the schedule and can be time consuming if an officer must take a sudden leave of absence and the scheduler must make several calls in order to find a replacement. This process can evolve with SmartBeats, a cloud-based service that can assist in scheduling police patrol areas.

# Description

## Problem
Each year the Glendale Police Department updates their patrol beats in order to improve response times and ensure that resources are placed where they are needed. As Glendale grows and changes, the needs of the community change. One area may have higher rates of traffic than it did last year, slowing down response time, or something else may have changed that makes it harder for Glendale Police to serve their community. This year they approached the Arizona State University Smart City Cloud Innovation Center (ASU CIC) for a solution in restructuring the beats. The ASU CIC seeks to build a solution that produces beat schedules that optimize response time and puts resources that are needed.

## Approach
Using data analytics, the ASU CIC will produce SmartBeats, a cloud-based software prototype that takes into account factors such as calls-for-services, incident information, disposition data and more in order to create optimal options for police schedules and beats. SmartBeats will help optimize schedules in less than optimal conditions, such as when an officer is out on leave. It can also help officers accomplish the department goal of spending a third of their time responding to calls, another third doing administrative tasks, and the final third being available and engaging with their community. The goal is to ensure a safe and timely response, provide more resources to communities, and increase community engagement to build better relationships with the community.

## Architecture Diagram

## Functionality

The functionality of Smartbeats is divided into two services:

### 1. Data Ingestion Service
Smartbeats require two input files to generate beats: 
1. City shapefile which contains City area divided into neighborhoods/polygons
2. Crime data in .csv format (We'll also provide the exact format of all required columns)


### 2. Spatial Data Processing Service
User can generate beats using a variety of different parameter options:
1. Beat creation criteria
2. Type of data to use (Calls-for-service/Incident data)
3. Priority
4. Disposition type
5. Start date and time
6. End date and time


## Technologies
Smartbeats is developed using a microserivce based architecture. It has two components, a web-tier and an app-tier. The web-tier hosts the frontend and the data ingestion service. The app-tier runs ArcGIS Pro for spatial data processing and generating beats.

We have used the following technologies to develop the application:

### Web-Tier
1. Python + [Django](https://www.djangoproject.com/): Application Development
2. [Amazon S3](https://aws.amazon.com/s3/): To store crime .csv and city shapefile
3. [Amazon Aurora](https://aws.amazon.com/rds/aurora/): To store data in crime .csv file
4. [Amazon EC2](https://aws.amazon.com/ec2/): Deployment of web-tier
5. [Pandas](https://pandas.pydata.org/): Data preprocessing
6. [GeoPandas](https://geopandas.org/): Spatial joins and geo-processing
7. [Folium](https://python-visualization.github.io/folium/): Visualization of generated beats map

### App-Tier
1. Python + [Flask](https://flask.palletsprojects.com/en/2.0.x/): Application Development
2. [Amazon S3](https://aws.amazon.com/s3/): To store beats shapefile
3. [ArcGIS Pro](https://pro.arcgis.com/en/pro-app/latest/get-started/get-started.htm): Spatial data processing
4. [Amazon EC2](https://aws.amazon.com/ec2/): Windows EC2 to host ArcGIS Pro and deploy App server

<!-- ## Challenges
1. To generate the exact  -->


## Assumptions
1. We have provided the sample [Crime csv](https://github.com/ASUCICREPO/smart-beats/blob/master/web-tier/beats/static/beats/example.csv) file that is required to generate beats. We are expecting the input file to be in the exact format.
2. Our application will not perform Geo-coding (the process of converting addresses into geographic coordinates). It has to be done on user end to create Crime csv file.
3. We are using ArcGIS Pro: buildBalancedZones() API in the backend. The user must have an active ArcGIS Pro subscription in the application server.
4. All spatial components (Geometry) like Points and Polygons in the input files (City shapefile + Crime csv) must have `epsg:4326`


## Future Enhancements
1. Overlaying beats map with real time police officer location information
2. Real-time manual manipulation of the generated Beats map
3. Include more beat generation parameters
4. Utilize ArcGIS Pro server licensing to scale app-tier
5. Deploy application on AWS Beanstalk (PaaS) or AWS Lambda (FaaS)
6. Create an email notification service to notify the user when the beat generation process is complete
7. Store history of generated beats
8. Color coding beats based on incident resolution data.
9. Use information such as phone calls, traffic data and CCTV footage to analyze and generate better beats.

<!-- # Installation Guide
## Web-Tier

# How to use


# Credits -->

# License
This project is distributed under the [Apache License 2.0](https://github.com/ASUCICREPO/smart-beats/blob/master/LICENSE)