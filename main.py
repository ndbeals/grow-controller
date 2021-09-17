
import time
import asyncio
from config import settings
from typing import Type

import outputs
import inputs

import threading

from log import log

from time import time as _time

def load_inputs(config_list: [dict]) -> None:
    device_list = []

    for conf in config_list:
        device_class = inputs.RegisteredDevices[conf.device]

        device = device_class( **conf )

        device_list.append(device)

    return device_list


class Trigger():
    def __init__(self, name: str, code: str) -> None:
        self.valid = False
        self.name = name
        self.code = code

        self.compileCode()

    def compileCode(self) -> None:
        try:
            self.compiled = compile( self.code, self.name, 'exec' )
            self.valid = True
        
        except SyntaxError as ex:
            log.error(ex)
            self.valid = False

    def run(self, global_vars: dict, local_vars: dict) -> None:
        try:
            if self.valid:
                exec(self.compiled, global_vars, local_vars)
            else:
                log.error("Trying to execute an invalid trigger ", self.name)

        except Exception as ex: #Catch all exceptions since we dont know what exception trigger code may raise
            log.error(f'Error in Trigger({self.name}): {ex}')
            # self.valid = False

class Application():
    
    def __init__(self) -> None:

        # self.read_tasks = []
        # self.input_devices = []
        self.input_devices = {}
        self.input_threads = {}

        self.output_devices = {}

        self.running = False
        self.trigger_task = None
        self.trigger_eval_period = 1
        self.triggers = {}
        self.trigger_globals = {}
        self.trigger_locals = {}


    def addInputTask(self, input_device: Type[inputs.InputBase]):
        device_name = input_device.name

        if self.input_threads.get(device_name):
            raise Exception("Task already exists.")

        else:
            self.input_threads[device_name] = input_device.readLoopThread()


    def loadInputDevices(self, config_list):
        for conf in config_list:
            device_class = inputs.RegisteredDevices[conf.device]

            device = device_class( **conf )

            # self.input_devices.append(device)
            self.input_devices[ conf.name ] = device

            self.addInputTask(device)

    def loadOutputDevices(self, config_list):
        for conf in config_list:
            device_class = outputs.RegisteredOutputs[conf['device']]

            device = device_class( **conf )
            # print("loading device ",conf)

            self.output_devices[ conf['name'] ] = device

    def loadTriggers(self, config_list):
        for conf in config_list:
            trigger = Trigger(conf.name, conf.code)

            self.triggers[ conf.name ] = trigger


    def setupTriggers(self):
        """Set up and populate global and local environments for triggers execution environment"""
        self.trigger_globals.update( self.output_devices )
        self.trigger_globals.update( self.input_devices )


    def runTriggers(self):
        for trigger in self.triggers.values():
            trigger.run( self.trigger_globals, self.trigger_locals )


    def start(self):
        self.loadInputDevices(settings.inputs)

        self.loadOutputDevices( settings.outputs )

        self.loadTriggers(settings.triggers)
        self.setupTriggers()

        self.running = True

        self.trigger_task = asyncio.create_task( self.run(), name="check_triggers")


    async def run(self):
        # print("waiting b4 run")
        await asyncio.sleep(5) # wait for a bit so input devices can populate their sensor data fields
        # TODO Implement threading.barrier here instead?

        # print("running triggers now")
        while self.running:
            self._next_trigger_eval = _time() + self.trigger_eval_period

            self.runTriggers()

            await asyncio.sleep( max(self._next_trigger_eval - _time(), 0.05) )




def devpr(a):
    while True:
        print(a,a.temperature,a.humidity,threading.current_thread())
        time.sleep(2)

async def main():
    app = Application()

    app.start()

    # app.loadInputDevices( settings.inputs )
    # await asyncio.sleep(0)
    # await asyncio.sleep(7.1)

    # app.loadTriggers( settings.triggers )
    # app.setupTriggers()
    # app.runTriggers()


    # a = app.input_devices['Hygrometer-1']

    # t = threading.Thread(target=devpr,args=(a,),daemon=True)
    # t.start()
    

    # input_devices = load_inputs(settings.inputs)

    # a = input_devices[0]

    # asyncio.create_task( a._readLoop() )


    await asyncio.sleep(1)

    # print("in main: ",a.temperature,a.humidity)

    print("exiting.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    loop.run_until_complete(main())

    # print("run_until_complete is done")

    loop.run_forever()