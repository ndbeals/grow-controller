import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn

from inputs import InputBase

from log import log


class ADS1115(InputBase):

    def __init__(self, name: str, device: str, channels: dict, **kwargs) -> None:
        super().__init__(name=name, device=device, **kwargs)

        # self.channels_conf = channels

        self.i2c = busio.I2C(board.SCL, board.SDA,frequency=100000)
        
        self.ads = ADS.ADS1115(self.i2c)

        self.channels = {}
        self.readers = []
        for chan_conf in channels:
            chan = AnalogIn(self.ads, chan_conf['pin'] )
            self.channels[ chan_conf['name'] ] = chan

            if chan_conf.get('normalize'):
                def read_chan():
                    val = chan.value / chan_conf['normalize']
                    setattr(self, chan_conf['name'], val )
            else:
                read_chan = lambda: setattr(self, chan_conf['name'], chan.value )
        self.readers.append(read_chan)
            

    def read_channel(self, name, channel):
        # print("read_chan ",name,channel)

        # self[ name ] = channel.value
        setattr(self, name, channel.value )

    def readInput(self):
        for name, chan in self.channels.items():
            self.read_channel( name, chan )