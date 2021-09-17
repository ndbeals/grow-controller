
RegisteredOutputs = {}

class OutputBase():

    def __init__(self, name:str = "uninitialized input device", device:str = "uninitialized device", **kwargs) -> None:

        # kwargs.update(kwargs['data'])
        # print("outputbase init ",kwargs)
        # del kwargs['data']

        super().__init__(**kwargs)

        self.name = name
        self.device = device
        pass

    def __init_subclass__(cls) -> None:
        RegisteredOutputs[ cls.__name__.lower() ] = cls