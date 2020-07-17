import boto3
from decouple import config

sqs = boto3.setup_default_session(region_name='us-east-1')
# Get the service resource:
sqs = boto3.resource('sqs',
                     aws_access_key_id=config('ACCESS_ID'),
                     aws_secret_access_key=config('ACCESS_KEY'))
# Get the queue:
queue = sqs.get_queue_by_name(QueueName='LightQueue.fifo')

def applySceneSQS(scene):
    print("Sending scene to RPi with SQS")
    response = queue.send_message(
        MessageBody = scene,
        MessageGroupId='scenes'
    )
