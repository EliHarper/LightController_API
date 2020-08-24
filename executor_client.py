
""" Implementation of the GRPC message.Executor client."""

from __future__ import print_function
from bson import ObjectId
import json
import logging

import grpc
from google.protobuf import json_format

import message_pb2
import message_pb2_grpc


CHANNEL_ADDRESS = '192.168.1.118:50051'

LOGGER_NAME =  'client_logger'
LOG_LOCATION = 'log/gRPC_Client.log'

class JSONEncoder(json.JSONEncoder):
    """ Converts BSON from the DB to functional JSON. 
          BSON ObjectIds can be problematic if not stringified. """
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def configure_logger(name: str, filepath: str, logLevel: int) -> logging.Logger:
    logger = logging.getLogger(name)
    handler = logging.FileHandler(filepath)

    logger.addHandler(handler)
    logger.setLevel(logLevel)

    return logger


def send_grpc(msg):
    # NOTE: .close() is possible on a channel and should be
    #   used in circumstances in which the 'with' statement does not fit the needs
    #   of the code.
    logger = configure_logger(LOGGER_NAME, LOG_LOCATION, logging.DEBUG)

    json_msg = JSONEncoder().encode(msg)
    proto_message = json_format.Parse(json_msg, message_pb2.ChangeRequest())
    with grpc.insecure_channel(CHANNEL_ADDRESS) as channel:
        stub = message_pb2_grpc.ExecutorStub(channel)
        response = stub.ApplyChange(proto_message)
        logger.debug('response received by client after sending msg {} in send_grpc: {}'.format(msg, response))

    return response


# if __name__ == '__main__':
#     logging.basicConfig()
#     run()
