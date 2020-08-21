
"""The Python implementation of the GRPC message.Executor client."""

from __future__ import print_function
from bson import ObjectId
import json

import grpc
from google.protobuf import json_format

import message_pb2
import message_pb2_grpc




class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def send_grpc(msg):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    json_msg = JSONEncoder().encode(msg)
    proto_message = json_format.Parse(json_msg, message_pb2.ChangeRequest())
    with grpc.insecure_channel('192.168.1.118:50051') as channel:
        stub = message_pb2_grpc.ExecutorStub(channel)
        response = stub.ApplyChange(proto_message)
        print('response received by client after sending msg {} in send_grpc: {}'.format(msg, response))

    return response


# if __name__ == '__main__':
#     logging.basicConfig()
#     run()
