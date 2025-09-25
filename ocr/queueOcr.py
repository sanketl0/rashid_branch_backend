import boto3
import json
import os
from django.conf import settings

sqs = boto3.client(
    'sqs',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS'),
    region_name='ap-south-1'
)


def send_message_to_queue(message,key,group):

    response = sqs.send_message(
        QueueUrl=settings.QUEUE_URL,
        MessageBody=str(message),
        MessageGroupId=group,
        MessageDeduplicationId=str(key)  # Required if ContentBasedDeduplication is false
    )
    print(response)