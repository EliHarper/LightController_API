
"""A Python implementation of my GRPC message.Executor server."""

from concurrent import futures
import logging

import grpc
from google.protobuf.json_format import MessageToDict

import message_pb2
import message_pb2_grpc
from .light import message_handler


class Executor(message_pb2_grpc.ExecutorServicer):

    def ApplyChange(self, request, context):
        # Hit the message_handler function:
        #   (also move paint_static_colors into animation_handler and get rid of animated bool)
        print('in ApplyChange(); request: {}'.format(request))
        message = MessageToDict(request)
        print('message: {}\nNow hitting message_handler.'.format(message))
        message_handler(message['json'])
        return message_pb2.ChangeReply(message='success')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_pb2_grpc.add_ExecutorServicer_to_server(Executor(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Started server.')
    server.wait_for_termination()


# Unused at the moment; not utilizing gRPC server logging (yet):
if __name__ == '__main__':
    logging.basicConfig()
    serve()
