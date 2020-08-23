
class SceneMessage:
    def __init__(self, Id: str, name: str, colors: list, defaultBrightness: float, functionCall: str,
                 index: int, animated: bool = False, animation: str = None):
        self.Id = Id
        self.name = name
        self.colors = colors
        self.defaultBrightness = defaultBrightness
        self.functionCall = functionCall
        self.index = index
        self.animated = animated
        self.animation = animation



class AdministrativeMessage:
    def __init__(self, functionCall='off', value=''):
        self.functionCall = functionCall
        self.value = value
