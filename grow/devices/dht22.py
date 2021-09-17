"""DHT22 humidity and temperature sensor"""

# from inputs.base import InputBase
# from inputs.base import InputBase
# from .base import InputBase
# from inputs import InputBase
from devices.base import InputBase

import threading
import time
import board
import adafruit_dht
import queue

from config import settings
from log import log

# Initial the dht device, with data pin connected to:
# dhtDevice = adafruit_dht.DHT22(board.D10)
# dhtDevice = adafruit_dht.DHT22(settings.dht_pin)
# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython. -> dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

def read_dht( dhtDevice ):
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        # print(
        #     "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
        #         temperature_f, temperature_c, humidity
        #     )
        # )

        return (temperature_c,humidity)

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0],error,error.args)

        # Wait and then re-run this function until it returns good data
        time.sleep(2.0)
        return read_dht( dhtDevice )
        
    except Exception as error:
        dhtDevice.exit()
        raise error

# __all__ = [read_dht]


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
            self.temperature = self.dht.temperature
            self.humidity = self.dht.humidity

            # print(self.temperature,self.humidity)
        
        except RuntimeError as ex:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            log.info( ex )
        
        except Exception as ex:
            self.dht.exit()
            time.sleep(1)
            del self.dht
            self.dht = adafruit_dht.DHT22(self.pin)


    # def readInput(self):
    #     data = read_dht(self.dht)
    #     print(time.time(),"read input device ",data)
    #     # print("read input device ",data,threading.current_thread(),self)

    #     self.temperature = data[0]
    #     self.humidity = data[1]

    #     return data

    # def __init_subclass__(cls) -> None:
    #     print("dht22 init_subclass", cls)
    #     # print(self.__name__)
    #     return super().__init_subclass__()