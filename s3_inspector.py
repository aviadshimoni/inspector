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

STRING = 'a'


class Inspector:

    def __init__(self):
        # creates all needed arguments for the program to run
        parser = argparse.ArgumentParser()
        parser.add_argument('-e', '--endpoint-url', help="endpoint url for s3 object storage", required=True)
        parser.add_argument('-a', '--access-key', help='access key for s3 object storage', required=True)
        parser.add_argument('-s', '--secret-key', help='secret key for s3 object storage', required=True)
       
        # parsing all arguments
        args = parser.parse_args()

        # building instance vars
        self.statuspageurl = 
        self.endpoint_url = args.endpoint_url
        self.access_key = args.access_key
        self.secret_key = args.secret_key
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
            print("S3 Service is UP")
            
        except requests.ConnectionError:
            

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

    #def notifytostatuspage(self, requestcheck, g_latency, p_latency, p_object, g_object):


if __name__ == '__main__':

    # Creates an instance
    inspector = Inspector()

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

    # checks for get and put latency
    get_latency = inspector.time_operation('GET', object_name, "")
    put_latency = inspector.time_operation('PUT', object_name, "")

    print(get_latency)
    print(put_latency)
    # compares between the latency and the threshold
