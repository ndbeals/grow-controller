# from __future__ import annotations
import threading
import time
# from inputs import RegisteredDevices
from typing import Type, List
from collections import deque

class DeviceBase():
    pass

class InputBase(DeviceBase):
    # RegisteredDevices: List[Type[InputBase]] = []
    RegisteredDevices = {}
    
    def __init__(self, name:str = "uninitialized input device", poll_interval:int=1, history_size:int=200, **kwargs) -> None:
        self.name = name
        # self.device = device
        
        # self.loop = asyncio.get_running_loop()
        self.poll_interval = poll_interval
        self.history_size = history_size
        # self.state = ()
        # print("base_init")
        # self.config = {}
        
        self.readLoopThread()

    def __init_subclass__(cls) -> None:
        # print("base init subclass",cls)
        InputBase.RegisteredDevices[ cls.__name__.lower() ] = cls
        # InputBase.RegisteredDevices.append(cls)

    def setSensorReading(self, name, value):
        # print('sensor read',name,value)
        if not hasattr(self, f'{name}_history'):
            setattr(self, f'{name}_history', deque(maxlen=self.history_size))

        getattr(self, f'{name}_history').append(value)
        setattr(self, name, value)

    def readInput(self):
        pass

    def readLoopThread(self):
        task = threading.Thread(target=self._readLoop, name=f'read_loop:{self.name}',daemon=True)
        task.start()
        self.read_task = task
        return task
    
    def _readLoop(self) -> None:
        time.sleep(0.5)
        while True:
            self._next_read_time = time.time() + self.poll_interval
            self.readInput()
            # print(time.time(),"read loop: ")
            # print("read loop: ",data,threading.current_thread())

            time.sleep( max(self._next_read_time - time.time(),0.1))



RegisteredOutputs = {}

class OutputBase(DeviceBase):

    def __init__(self, name:str = "uninitialized input device", **kwargs) -> None:

        # kwargs.update(kwargs['data'])
        # print("outputbase init ",kwargs)
        # del kwargs['data']

        super().__init__(**kwargs)

        self.name = name
        # self.device = device
        pass

    def __init_subclass__(cls) -> None:
        RegisteredOutputs[ cls.__name__.lower() ] = cls