# from log import log
# print("logic.py load")
import schedule
import time
from time import time as now

# from devices import DHT22, ADS1115
import devices
from log import log

from util import StateTable
import util
# print(DHT22)

hygrometer = devices.DHT22(10,2)

adc_1 = devices.ADS1115(channels=[
    {
        'name': 'water_level',
        'pin': 0
    }
])

mist_relay = devices.Relay(pin=17, active_high=False, initial_value=False)
pump_relay = devices.Relay(pin=27, active_high=False, initial_value=False)

def timed_wait(_time, duration):
    return (_time + duration) < time.time()


# last_humidified = 0
state_hum = StateTable()
state_hum.last_humidified = 0
state_hum.shutoff_at = 0
state_hum.shutoff_wait = False
def check_humidity():
    global state_hum
    humidity = util.simple_moving_average(hygrometer.humidity_history, 30 )
    # print(humidity, hygrometer.humidity)

    if humidity < 85 and timed_wait(state_hum.last_humidified, 1800):
        log.success("turning fogger on.")
        print(humidity, hygrometer.humidity)
        mist_relay.on()

        state_hum.last_humidified = time.time()


    if humidity > 95:
        if not state_hum.shutoff_wait:
            state_hum.shutoff_wait = True
            state_hum.shutoff_at = time.time() + 1*60
        
        if state_hum.shutoff_wait and state_hum.shutoff_at < now():
            state_hum.shutoff_wait = False

            log.success('turning fogger off')
            print(humidity, hygrometer.humidity)
            mist_relay.off()
        
schedule.every(1).seconds.do(check_humidity)


# state_water = StateTable()
# state_water.
def check_water_level():

    water_level = util.simple_moving_average( adc_1.water_level_history, 50 )
    # print('water lev: ',water_level,adc_1.water_level)

    if water_level < 9500:
        # log.success('turning pump on')
        pump_relay.on()

    if water_level > 10500:
        # log.success('turning pump off')
        pump_relay.off()

schedule.every(1).seconds.do(check_water_level)


time.sleep(5)
while True:
    schedule.run_pending()
    time.sleep(0.1)