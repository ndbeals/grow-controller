import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA,frequency=100000)

# Create the ADC object using the I2C bus
# ads = ADS.ADS1015(i2c)
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

# ads.gain =2/3
# ads.gain = 2
# print(ads.gain)

# print(i2c.try_lock())
# i2c.try_lock()
while not i2c.try_lock():
    pass

count = 0
print("Scanning I2C bus")
for x in i2c.scan():
    print(hex(x))
    count += 1


print("locked")
i2c.unlock()
# ads.mode = Mode.CONTINUOUS
# ads.data_rate = 8
print("{:>5}\t{:>5}".format('raw', 'v'))

wait_time = 1/ads.data_rate

try:
    while True:
        print("{:>5}\t{:>5.6f}".format(chan.value, chan.voltage))
        time.sleep(wait_time)
        # time.sleep(1)
except KeyboardInterrupt:
    i2c.unlock()