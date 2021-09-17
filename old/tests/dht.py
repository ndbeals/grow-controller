
# import Adafruit_DHT

# DHT_SENSOR = Adafruit_DHT.DHT22
# DHT_PIN = 10


# try:
#     while True:
# #        print(1)
#         humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
# #        print(2)
#         if humidity is not None and temperature is not None:
#             print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
#         else:
#             print("Failed to retrieve data from humidity sensor")

# except KeyboardInterrupt:
#     print("quit.")


import time
import board
import adafruit_dht

# Initial the dht device, with data pin connected to:
# dhtDevice = adafruit_dht.DHT22(board.D18)
dhtDevice = adafruit_dht.DHT22(board.D10)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)