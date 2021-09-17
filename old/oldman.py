import asyncio
import time
from typing import Coroutine, List
from collections import deque

import concurrent.futures
import threading
import queue

import dht

import inputs
print(inputs.InputBase)

def simple_moving_average(seq, n):
    average = 0
    c = 0

    for i in range(len(seq),max(len(seq)-n,0),-1):
        # print(i)
        average += seq[i-1]
        c+=1
    
    average = average / c
    return average


class GrowController():
    tasks: List[asyncio.Task]
    # humidityHistory

    def __init__(self) -> None:
        self.loop = asyncio.get_running_loop()
        self.tasks = []

        # self.threadPool = 
        self.humidityHistory = deque(maxlen=60)
        # self.tempHistory = []

    def addTask(self, task: asyncio.Task):
        self.tasks.append(task)

    def createTask(self, task: Coroutine):
        task = asyncio.create_task(task)
        self.addTask(task)

    async def exit(self):
        for task in self.tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                print(f"main(): {task} is cancelled now")

    async def read_dht(self):
        self.createTask(self.read_dht_loop())

    async def read_dht_loop(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            while True:
                self._next_dht_time = time.time() + 2
                data = await self.loop.run_in_executor(executor, dht.read_dht)

                asyncio.create_task(self.updateTempHumid(data))

                await asyncio.sleep( max(self._next_dht_time - time.time(),1) )

    # async def controllerLogic(self):
    async def updateTempHumid(self, data):
        if data:
            temperature = data[0]
            humidity = data[1]

            self.humidityHistory.append(humidity)

            a = simple_moving_average(self.humidityHistory,5)
            print("avg: ",a)

            # print("new temp and hum ",temperature,humidity)


# def get_dht(a,b):
#     print("got dht in a thre")

async def long( a ):
    t = time.time()
    print("threads: ",threading.active_count())
    print(f"async func: {a}")
    await asyncio.sleep(3)
    print(f"async func: {a} - elapsed: {time.time()-t}")
    print("threads: ",threading.active_count())
    # print("async func: ",a)


async def dht_loop_read():
    loop = asyncio.get_running_loop()
    while True:
        # data = queue.get(block=False)
        # data = queue.get_nowait()
        t=time.time()
        # data = dht.read_dht()
        data = await loop.run_in_executor(None,dht.read_dht)
        print(f"time: {round(time.time()-t,4)}  data: {data}")
        await asyncio.sleep(2)
        # print("after sleep and get")


async def main():

    # print("async main")
    # q = queue.Queue()
    # dht_thread = threading.Thread(target=dht.dht_loop,args=(q,),daemon=True)
    # dht_thread.start()

    app = GrowController()
    await app.read_dht()

    # app.createTask(dht_loop_read())
    # task = asyncio.create_task(dht_loop_read())
    # await dht_queue(q)
    # print("eh?")

    # await long(1)
    # print("after 1")

    # await long(2)
    # print("after 2")
    # await long(3)
    # print("after 3")
    # await long(4)
    # print("after 4")

    # await app.exit()

    # await dht_queue(q)
    # print("after 3")




if __name__ == "__main__":
    # print("as")
    loop = asyncio.get_event_loop()

    loop.run_until_complete(main())

    print("run_until_complete is done")

    loop.run_forever()