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
        self.bucket_name = config.bucket_name #inspector_bucket
        
    # tries to connect to redis using redis sdk, if can't - exits and prints a message 
    def connects_to_redis(self):
        try:
            self.redisconnection = redis.Redis(host=self.redishost, port=6379, db=0)
        except Exception as ex:
            print ('Error:', ex)
            exit('Failed to connect to the redis host, terminating')

    # tries to connect to ceph cluster using boto3, if can't - exits and prints a message
    def connects_to_s3(self):
        try:
            self.s3 = boto3.client('s3', endpoint_url=self.endpoint_url, aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        except Exception as ex:
            self.notify_cachet_curl()
            self.notify_cachet_get_performance(maj_out)
            self.notify_cachet_put_performance(maj_out)
            print  ('Error:', ex)
            exit('Failed to connect to Ceph Cluster using boto3, terminating')

    # tries to connect to cachet using cachet sdk, if can't - exit and prints a message
    def connects_to_cachet(self):
        try:
            self.components =  cachet.Components(endpoint = self.statuspage,
            api_token = self.cachet_token)
        except Exception as ex:
            print ('Error:', ex)
            exit('Failed to connect to Cachet using Cacht SDK, terminating')

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
    def get_object(self, object_name):
        response = self.s3.get_object(Bucket=self.bucket_name, Key=object_name)
        response['Body'].read()

    # Creates data from the memory for the Ceph object
    def create_bin_data(self, object_size):
        return humanfriendly.parse_size(object_size) * STRING
    
    # checks 10 last arguments latency on the database and returns True if all of them are greater than 2sec latency
    def redis10(self, access_method, size):
        if access_method == 'GET':
            getlatencyarray = self.redisconnection.lrange('getlist' + size, -10, 50000000)
            for latency in getlatencyarray:
                if float(latency) < 2:
                    return True
        elif access_method == 'PUT':
            putlatencyarray = self.redisconnection.lrange('putlist' + size, -10, 5000000)
            for latency in putlatencyarray:
                if float(latency) < 20:
                    return True
        return False

    # generates random object name based on basename, object size and date
    def randomize_name(size):
        basename = "inspector_" + size 
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        object_name = "_".join([basename, suffix]) # e.g. 'inspector_object_120508_171441'
        return object_name
    
    # changes the S3 Object Service status to Major Outage
    def notify_cachet_curl(self):
        self.components.put(id=1, status=maj_out)

    # changes the Get Performance component status to Performance Issues / Good Performance based on Access Method & Object Size
    def notify_cachet_performance(self, statusnum, size, access_method):
        if accesss_method == 'GET':
            # object size  = 16KB
            if size == '16KB':
                self.components.put(id=2, status=statusnum) # 16KB Get Performance component ID = 2
            # object size = 128KB
            elif size == '128KB':           
                self.components.put(id=3, status=statusnum) # 128KB Get Performance component ID = 3
            # object size = 512KB
            elif size == '512KB':
                self.components.put(id=4, status=statusnum) # 512KB Get Performance component ID = 4
            # object size = 1MB
            elif size == '1MB':
                self.components.put(id=5, status=statusnum) # 1MB Get Performance component ID = 5
             # object size = 2MB
            elif size = '2MB':
                self.components.put(id=6, status=statusnum) # 2MB aGet Performance component ID = 6
            # object size = 32MB
            elif size = '32MB'
                self.components.put(id=7, status=statusnum) # 32MB Get Performance component ID = 7

        elif access_method == 'PUT':
            # object size  = 16KB
            if size == '16KB':
                self.components.put(id=8, status=statusnum) # 16KB Get Performance component ID = 8
            # object size = 128KB
            elif size == '128KB':
                self.components.put(id=9, status=statusnum) # 128KB Get Performance component ID = 10
            # object size = 512KB
            elif size == '512KB':
                self.components.put(id=10, status=statusnum) # 512KB Get Performance component ID = 9 
            # object size = 1MB
            elif size == '1MB':
                self.components.put(id=11, status=statusnum) # 1MB Get Performance component ID = 11
            # object size = 2MB
            elif size = '2MB':
                self.components.put(id=12, status=statusnum) # 2MB aGet Performance component ID = 12
            # obejct size = 32MB
            elif size = '32MB'
                self.components.put(id=13, status=statusnum) # 32MB Get Performance component ID = 13


if __name__ == '__main__':
    # cachet components global vars which will be used to describe component status

    # majoroutage - large component which affect all the service
    maj_out = 4
    
    # good performance of a component
    good_perf = 1
    
    # degraded performance of a component
    deg_perf = 2 
    
    # Creates an instance
    inspector = Inspector()
    
    # Connects to s3
    inspector.connects_to_s3()
    
    # Connects to redis
    inspector.connects_to_redis()
    
    # Connects to cachet
    inspector.connects_to_cachet()
    
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
    
    for size in config.object_size:

        # Creates binary data
        data = inspector.create_bin_data(size)
    
        # Creates a random object name 
        object_name = randomize_name(size)

        # test upload, if doesn't work, update S3 cachet component
        try:
            inspector.put_object(object_name, bin_data=data)
        except Exception as ex:
            print ('Error', ex)
            inspector.notify_cachet_curl()

        # True of False, checks for http response
        if inspector.inspector_curl() is not True:
            inspector.notify_cachet_curl()

        # checks for get and put latency
        get_latency = inspector.time_operation('GET', object_name, "")
        put_latency = inspector.time_operation('PUT', object_name, data)

        # pushs them to a redis lists based on access method and object size
        inspector.redisconnection.rpush("getlist" + size, get_latency)    
        inspector.redisconnection.rpush("putlist" + size, put_latency)
   
        ### Checks 10 last arguments in the redis db based on the access method

        if inspector.redis10('GET', size) is True:
            inspector.notify_cachet_performance(good_perf, size, 'GET')
        else:
            inspector.notify_cachet_performance(deg_perf, size, 'GET')
        # if redis10 returns True, means that put performance is good, sets performance to O.K, else, degreded.
        if inspector.redis10('PUT', object_size) is True:
            inspector.notify_cachet_performance(good_perf, size, 'PUT')
        else:
            inspector.notify_cachet_performance(deg_perf, size, 'PUT')
        
