#!/usr/bin/env python3

'''
@Author Aviad Shimoni
@Date   18/08/2019
'''
import argparse
import requests
import boto3
import datetime
from botocore import endpoint
from botocore.exceptions import ClientError
import humanfriendly
import cachetclient
from cachetclient.v1 import enums
from cachetclient.v1 import components


STRING = 'a'


class Inspector:

    def __init__(self):
        # creates all needed arguments for the program to run
        parser = argparse.ArgumentParser()
        parser.add_argument('-e', '--endpoint-url', help="endpoint url for s3 object storage", required=True)
        parser.add_argument('-a', '--access-key', help='access key for s3 object storage', required=True)
        parser.add_argument('-s', '--secret-key', help='secret key for s3 object storage', required=True)
        parser.add_argument('-c', '--cachet-token', help='secret key for cachet client status page', required=True)
        # parsing all arguments
        args = parser.parse_args()

        # building instance vars
        self.statuspage = 'http://status.test/api/v1'

        self.endpoint_url = args.endpoint_url
        self.access_key = args.access_key
        self.secret_key = args.secret_key
        self.cachet_token = args.cachet_token
        self.bucket_name = 'inspector_bucket'
        self.object_size = '1MB'
        self.object_name = 'inspector_test_object'
        self.s3 = boto3.client('s3', endpoint_url=self.endpoint_url, aws_access_key_id=self.access_key,
                               aws_secret_access_key=self.secret_key)

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

    # Checks for http response
    def inspector_curl(self):
        try:
            _ = requests.get(self.endpoint_url, timeout=5)
            return True
        except requests.ConnectionError:
            print "Connection Error"
            return False
            

    # Puts object on the s3
    def put_object(self, name, bin_data):
        self.s3.put_object(Key=object_name, Bucket=self.bucket_name, Body=bin_data)

    # Gets object from the s3
    def get_object(self, name):
        response = self.s3.get_object(Bucket=self.bucket_name, Key=object_name)
        response['Body'].read()

    # Creates data from the memory for the Ceph object
    def create_bin_data(self):
        return humanfriendly.parse_size(self.object_size) * STRING
    
    def cachet_connect():
        client = cachetclient.Client(
            endpoint=self.statuspage
            api_token=self.cachet_token
            return client
        )

    def notify_cachet_curl(Client):
        Client.ComponentManager.update(component_id=1, status=4)

    def notify_cachet_get_performance(Client):
        Client.ComponentManager.update(component_id=2, status=4)

    def notify_cachet_get_performance(Client):
        Client.ComponentManager.update(component_id=3, status=4)
    

if __name__ == '__main__':

    # Creates an instance
    inspector = Inspector()

    cachet_connection = cachet_connect()

    # Creates a bucket for our script, if bucket's already exists, prints a message.
    try:
        inspector.s3.create_bucket(Bucket='inspector_bucket')
        'Bucket {} created!'.format("inspector")
    except ClientError:
        print("Bucket already exist, No need to create.")

    # Creates binary data
    data = inspector.create_bin_data()
    # sets the object's name
    object_name = 'inspector_test_object'

    # test upload
    inspector.put_object(object_name, bin_data=data)

    # test download
    inspector.get_object(object_name)

    # True of False, checks curl
    curl_check = inspector.inspector_curl()

    if !curl_check:
        notify_cachet_curl(cachet_connection)

    # checks for get and put latency
    get_latency = inspector.time_operation('GET', object_name, "")
    put_latency = inspector.time_operation('PUT', object_name, "")

    # compares between the latency and the threshold
    if ( get_latency >= 2 ):
        notify_notify_cachet_get_performance(cachet_connection)
    else:
        #make it green
        #sending to status page function
    
    if ( put_latency >= 2 ):
        notify_notify_cachet_put_performance(cachet_connection)
   
    