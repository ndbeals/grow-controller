# from __future__ import annotations
import threading
import time
# from inputs import RegisteredDevices
from typing import Type, List

# import asyncio
# import concurrent.futures

# thread_executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
# input_device_tasks = []

class InputBase():
    # RegisteredDevices: List[Type[InputBase]] = []
    RegisteredDevices = {}
    
    def __init__(self, name:str = "uninitialized input device", device:str = "uninitialized device", poll_interval:int=1, **kwargs) -> None:
        self.name = name
        self.device = device
        
        # self.loop = asyncio.get_running_loop()
        self.poll_interval = poll_interval
        # self.state = ()
        # print("base_init")
        # self.config = {}
        pass

    def __init_subclass__(cls) -> None:
        # print("base init subclass",cls)
        InputBase.RegisteredDevices[ cls.__name__.lower() ] = cls
        # InputBase.RegisteredDevices.append(cls)

    def readInput(self):
        pass

    def readLoopThread(self):
        task = threading.Thread(target=self.__readLoop, name=f'read_loop:{self.name}')
        task.start()
        return task
    
    def __readLoop(self) -> None:
        while True:
            self._next_read_time = time.time() + self.poll_interval
            # data = await self.loop.run_in_executor(executor, self.readInput)
            self.readInput()
            # print(time.time(),"read loop: ")
            # print("read loop: ",data,threading.current_thread())

            # asyncio.create_task(self.updateTempHumid(data))
            time.sleep( max(self._next_read_time - time.time(),0.1))
            # await asyncio.sleep( max(self._next_read_time - time.time(),0.1) )
    
    # async def _readLoop(self) -> None:
    #     with thread_executor as executor:
    #         while True:
    #             self._next_read_time = time.time() + self.poll_interval
    #             data = await self.loop.run_in_executor(executor, self.readInput)
    #             print("read loop: ",data)
    #             # print("read loop: ",data,threading.current_thread())

    #             # asyncio.create_task(self.updateTempHumid(data))

    #             await asyncio.sleep( max(self._next_read_time - time.time(),0.1) )