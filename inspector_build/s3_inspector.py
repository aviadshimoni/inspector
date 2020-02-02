'''
@Author Aviad Shimoni
@Date   18/08/2019
Script used by customers to define our S3 service quality
'''
import requests
import boto3
import datetime
import config
import os
import json
from botocore import endpoint
from botocore.exceptions import ClientError
import humanfriendly
import redis
import cachetclient.cachet as cachet

STRING = 'a'


class Inspector:

    def __init__(self):
        # building instance vars
        self.statuspage = 'http://'+config.cachet_host+':80/api/v1'
        self.endpoint_url = config.endpoint_url
        self.access_key = config.access
        self.secret_key = config.secret
        self.redishost = config.redis_host
        self.cachet_token = config.apitoken    
        self.bucket_name = 'inspector_bucket'
        self.object_size = '1MB'
        self.object_name = 'inspector_test_object'
        #try to connect to cachet using cachet sdk
        try:
            self.components =  cachet.Components(endpoint = self.statuspage,
            api_token = self.cachet_token)
        except Exception as ex:
            print ('Error:', ex)
            exit('Failed to connect to Cachet using Cacht SDK, terminating')
        #try to connect to ceph cluster using boto3
        try:
            self.s3 = boto3.client('s3', endpoint_url=self.endpoint_url, aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        except Exception as ex:
            self.notify_cachet_curl()
            self.notify_cachet_get_performance(4)
            self.notify_cachet_put_performance(4)
            print  ('Error:', ex)
            exit('Failed to connect to Ceph Cluster using boto3, terminating')
        #try to connect to redis using redis sdk
        try:
            self.redisconnection = redis.Redis(host=self.redishost, port=6379, db=0)
        except Exception as ex:
            print ('Error:', ex)
            exit('Failed to connect to the redis host, terminating')

    # returns action latency based on the method
    def time_operation(self, method, name, bin_data):
        if method == 'GET':
            start = datetime.datetime.now()
            self.get_object(name)
            end = datetime.datetime.now()
            diff = (end - start).total_seconds() * 1000

        elif method == 'PUT':
            start = datetime.datetime.now()
            self.put_object(name, bin_data)
            end = datetime.datetime.now()
            diff = (end - start).total_seconds() * 1000

        return diff

    # Checks for a http response
    def inspector_curl(self):
        try:
            _ = requests.get(self.endpoint_url, timeout=5)
            return True
        except requests.ConnectionError:
            print ("Connection Error")
            return False
    
    # Puts object on the s3
    def put_object(self, name, bin_data):
        self.s3.put_object(Key=object_name, Bucket=self.bucket_name, Body=bin_data)

    # Gets object from the s3
    def get_object(self, name):
        response = self.s3.get_object(Bucket=self.bucket_name, Key=self.object_name)
        response['Body'].read()

    # Creates data from the memory for the Ceph object
    def create_bin_data(self):
        return humanfriendly.parse_size(self.object_size) * STRING

    # checks 10 last arguments latency on the database and returns True if all of them are greater than 2sec latency
    def redis10(self, access_method):
        if access_method == 'GET':
            getlatencyarray = self.redisconnection.lrange('getlist', -10, 50000000)
            print(getlatencyarray)
            for latency in getlatencyarray:
                if float(latency) < 2:
                    return True
        elif access_method == 'PUT':
            putlatencyarray = self.redisconnection.lrange('putlist', -10, 5000000)
            for latency in putlatencyarray:
                if float(latency) < 20:
                    return True
        return False

    # changes the S3 Object Service status to Major Outage
    def notify_cachet_curl(self):
        self.components.put(id=1, status=4)
   
    # changes the Get Performance component status to Performance Issues / Good Performance
    def notify_cachet_get_performance(self, statusnum):
        self.components.put(id=2, status=statusnum)

    # changes the Put Performance component status to Performance Issues
    def notify_cachet_put_performance(self, statusnum):
        self.components.put(id=3, status=statusnum)
    
if __name__ == '__main__':

    # Creates an instance
    inspector = Inspector()
    # Creates a bucket for our script, if bucket's already exists, prints a message.
    try:
        inspector.s3.create_bucket(Bucket='inspector_bucket')
        'Bucket {} created!'.format("inspector")
    except ClientError:
        print("Bucket already exist, No need to create.")
    except Exception as ex:
        print ('Error', ex)
        inspector.notify_cachet_curl()
        exit('Failed to connect to Ceph Cluster using boto3, terminating')

    # Creates binary data
    data = inspector.create_bin_data()
    # sets the object's name
    object_name = 'inspector_test_object'

    # test upload
    try:
        inspector.put_object(object_name, bin_data=data)
    except Exception as ex:
        print ('Error', ex)
        inspector.notify_cachet_curl()
    # test download
    inspector.get_object(object_name)

    # True of False, checks for http response
    if inspector.inspector_curl() is not True:
        inspector.notify_cachet_curl()

    # checks for get and put latency
    get_latency = inspector.time_operation('GET', object_name, "")
    put_latency = inspector.time_operation('PUT', object_name, "")

    # pushs them to a redis list
    inspector.redisconnection.rpush("getlist", get_latency)    
    inspector.redisconnection.rpush("putlist", put_latency)
   
    ### Checks 10 last arguments in the redis db based on the access method

    # if redis10 returns True, means that get performance is good, sets performance to O.K, else, degreded. 
    if inspector.redis10('GET') is True:
        inspector.notify_cachet_get_performance(2)
    else:
        inspector.notify_cachet_get_performance(1)
    # if redis10 returns True, means that put performance is good, sets performance to O.K, else, degreded.
    if inspector.redis10('PUT') is True:
        inspector.notify_cachet_put_performance(2)
    else:
        inspector.notify_cachet_put_performance(1)
        
