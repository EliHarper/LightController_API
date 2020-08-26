
class SceneMessage:
    def __init__(self, dct):
        """ Construct with dictionary magic; each field in the dict is now that of an Object. """
        self.__dict__ = dct

    def __str__(self):
        return f'SceneMessage in dict format: {self.__dict__}'



class AdministrativeMessage:
    def __init__(self, functionCall='off', value=''):
        self.functionCall = functionCall
        self.value = value

    def __str__(self):
        return f'AdministrativeMessage functionCall: \"{self.functionCall}\". Value: {self.value}.'
