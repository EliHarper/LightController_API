import boto3
import json
from decouple import config
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



sqs = boto3.setup_default_session(region_name='us-east-1')
# Get the service resource:
sqs = boto3.resource('sqs',
                     aws_access_key_id=config('ACCESS_ID'),
                     aws_secret_access_key=config('ACCESS_KEY'))
# Get the queue:
queue = sqs.get_queue_by_name(QueueName='LightQueue.fifo')

def applySceneSQS(scene):
    print("Sending scene to RPi with SQS")
    scene_str = JSONEncoder().encode(scene)
    response = queue.send_message(
        MessageBody = scene_str,
        MessageGroupId='scenes'
    )
