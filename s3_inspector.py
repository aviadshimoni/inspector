'''
@Author Aviad Shimoni
@Date   18/08/2019
'''

import requests
import boto3
import botocore
from botocore import endpoint
from botocore.exceptions import ClientError


# import boto.s3.connection

def inspector_curl(url='http://127.0.0.1:8001', timeout=5):
    try:
        _ = requests.get(url, timeout=timeout)
        print("CURL IS UP!")
        return True
    except requests.ConnectionError:
        print("s3 service is not reachable.")
        return False


if __name__ == '__main__':
    access_key = 'RK224EIAHPE2BH7ZYIQW'  # Add your S3 Access Key here
    secret_key = 'QoHW1yt4OpvMjpnOuLse7cN3jKTgqz34cLMnzIsN'  # Add your S3 Secret Key here
    bucket_name = 'inspector'
    service_state = inspector_curl()
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key,
                      endpoint_url='http://127.0.0.1:8001')
    print(s3)
    s3.create_bucket(Bucket='inspector_bucket')
    'Bucket {} created!'.format("inspector")

    # declare some variables
    key = 'home/user/Desktop/inspector_check_upload'
    outputName = 'inspector_uploaded.txt'

    # test upload
    s3.upload_file('/home/user/Desktop/inspector_check_upload', "inspector", 'inspector_uploaded.txt')
    # test download
    try:
        s3.Bucket('inspector').download_file(key, outputName)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
