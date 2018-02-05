#nonstandard
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.s3.bucket import Bucket
from boto.exception import *
from boto.s3.connection import OrdinaryCallingFormat


def get_bucket_list(key, secret):
    s3 = S3Connection(aws_access_key_id=key, aws_secret_access_key=secret,
                is_secure=True, calling_format=OrdinaryCallingFormat())
    buckets=s3.get_all_buckets()
    result = []
    for b in buckets:
        result.append(b.name)
    return result
