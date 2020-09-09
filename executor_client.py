
""" Implementation of the gRPC message.Executor client."""

from __future__ import print_function
from bson import ObjectId
import json
import logging
import time

import grpc
from google.protobuf import json_format

import ambilight
import message_pb2
import message_pb2_grpc


CHANNEL_ADDRESS = '192.168.1.118:50051'

LOGGER_NAME =  'client_logger'
LOG_LOCATION = 'log/gRPC_Client.log'
logger = logging.getLogger(LOGGER_NAME)

ambi = ambilight.Ambilight()
AMBI_COUNT = 0

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


def convert_to_proto(msg):
    json_msg = JSONEncoder().encode(msg)
    proto_message = json_format.Parse(json_msg, message_pb2.ChangeRequest())

    return proto_message


def generate_colors():
    global logger
    global AMBI_COUNT

    logger = configure_logger(LOGGER_NAME, LOG_LOCATION, logging.DEBUG)

    while ambi.on:
        logger.debug('generating top colors..')
        top_colors = ambilight.run()
        logger.debug('top_colors = {}'.format(top_colors))

        tuple_protos = []
        for color in top_colors:
            tuple_proto = message_pb2.tuple_color(item=color)
            tuple_protos.append(tuple_proto)

        logger.debug('tuple_protos: {}'.format(tuple_protos))
        logger.debug('About to make the ColorsRequest')
        colors_req = message_pb2.ColorsRequest(color=tuple_protos)

        logger.debug('About to yield')
        yield colors_req
        logger.debug('Passed yield')


def forward_colors(stub):
    global ambi
    global logger

    ambi.on = True
    color_iterator = generate_colors()

    print('type(color_iterator): {}'.format(type(color_iterator)))
    summary = stub.ApplyAmbiLight(color_iterator)
    print(summary)
    # logger.debug('summary: {}'.format(summary.result()))



def send_grpc(msg):
    # NOTE: .close() is possible on a channel and should be
    #   used in circumstances in which the 'with' statement does not fit the needs
    #   of the code.
    logger = configure_logger(LOGGER_NAME, LOG_LOCATION, logging.DEBUG)

    proto_message = convert_to_proto(msg)
    with grpc.insecure_channel(CHANNEL_ADDRESS) as channel:
        stub = message_pb2_grpc.ExecutorStub(channel)
        response = stub.ApplyChange(proto_message)
        logger.debug('response received by client after sending msg {} in send_grpc: {}'.format(msg, response))

    return response


def send_stream():
    """ Applies ambient light via request-streaming gRPC """
    with grpc.insecure_channel(CHANNEL_ADDRESS) as channel:
        stub = message_pb2_grpc.ExecutorStub(channel)
        forward_colors(stub)



# if __name__ == '__main__':
#     logging.basicConfig()
#     run()
