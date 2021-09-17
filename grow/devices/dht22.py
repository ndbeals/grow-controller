"""DHT22 humidity and temperature sensor"""


from devices.base import InputBase

import threading
import time
import board
import adafruit_dht
import queue

# from config import settings
from log import log

# Initial the dht device, with data pin connected to:
# dhtDevice = adafruit_dht.DHT22(board.D10)
# dhtDevice = adafruit_dht.DHT22(settings.dht_pin)
# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython. -> dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)


class DHT22(InputBase):
    def __init__(self, pin:int, poll_interval:int=2, **kwargs ) -> None:
        super().__init__( **kwargs)

        self.poll_interval = poll_interval
        self.temperature = None
        self.humidity = None

        self.pin = pin
        self.dht = adafruit_dht.DHT22(pin)


    def readInput(self):
        try:
            # self.temperature = self.dht.temperature
            # self.humidity = self.dht.humidity
            self.setSensorReading('temperature',self.dht.temperature)
            self.setSensorReading('humidity',self.dht.humidity)

            # print(self.temperature,self.humidity)
        
        except RuntimeError as ex:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            log.info( ex )
        
        except Exception as ex:
            log.critical(ex)
            self.dht.exit()
            time.sleep(1)
            del self.dht
            self.dht = adafruit_dht.DHT22(self.pin)