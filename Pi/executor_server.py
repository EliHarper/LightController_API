
""" Implementation of my GRPC message.Executor server. """

from concurrent import futures

import grpc
import logging
from google.protobuf.json_format import MessageToJson, MessageToDict

import message_pb2
import message_pb2_grpc
from .light import message_handler, handle_ambilight
from .message import SceneMessage, AdministrativeMessage


# Global declarations:
LOGGER_NAME = 'server_logger'
LOG_LOCATION = 'log/gRPC_Server.log'
LOG_LEVEL = logging.DEBUG
logger = logging.getLogger(LOGGER_NAME)
# Dictionary key constants:
ID = 'Id'
FUNCTION_CALL = 'functionCall'
VALUE = 'value'


class Executor(message_pb2_grpc.ExecutorServicer):
    def ApplyChange(self, request, context):
        logger = configure_logger()
        # Hit the message_handler function:
        #   (also move paint_static_colors into animation_handler and get rid of animated bool)
        logger.debug('in ApplyChange(); request: {}'.format(request))
        # Use Google's protobuf -> Dict deserializer: 
        message = MessageToDict(request)
        # Then convert the Dict to a Python Object as one of the two types I've defined in message.py:
        message_object = self.ConstructMessage(message)
        logger.debug('message object constructed from Dict: {}'.format(message_object.__str__()))
        # Take the object & pass it to the message_handler in light.py:
        message_handler(message_object)
        return message_pb2.ChangeReply(message='success')


    def ApplyAmbiLight(self, request_iterator, context):
        logger = configure_logger()

        print('in ambilight.......................')
        logger.info('in ApplyAmbiLight(); request_iterator: {}'.format(request_iterator))
        # May not be necessary to deserialize to a dict; object should be an RGB array on reformat from string
        try:
            for tupley_list in request_iterator:
                logger.info('tupley_list: {}'.format(tupley_list))
                tuple_dict = MessageToDict(tupley_list)
                msg_obj = SceneMessage(tuple_dict)
                handle_ambilight(msg_obj)
        except grpc.__channel__.Rendezvous as err:
            logger.info('err: {}'.format(err))

        return message_pb2.ChangeReply(message='success')

    
    def ConstructMessage(self, message):
        # SceneMessages have Ids; AdministrativeMessages do not. Cast appropriately via duck typing:
        try:
            if ID in message:
                message_object = SceneMessage(message)
            elif VALUE in message:
                logger.debug('VALUE is in AdministrativeMessage')
                message_object = AdministrativeMessage(message[FUNCTION_CALL], message[VALUE])
            else:
                logger.debug('VALUE is not in AdministrativeMessage')
                message_object = AdministrativeMessage(message[FUNCTION_CALL])
        except Exception as e:
            logger.debug('Caught exception while in ConstructMessage of type {}: {}'.format(type(e), e))

        return message_object


def configure_logger() -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    handler = logging.FileHandler(LOG_LOCATION)

    logger.addHandler(handler)
    logger.setLevel(LOG_LEVEL)

    return logger


def serve():
    global logger

    logger = configure_logger()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_pb2_grpc.add_ExecutorServicer_to_server(Executor(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logger.info('Started server.')
    server.wait_for_termination()


# Unused at the moment - ExecutorServer is served by light.py.
# if __name__ == '__main__':
#     logging.basicConfig()
#     serve()
