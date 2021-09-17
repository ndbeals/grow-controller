
import Adafruit_DHT

import RPi.GPIO as GPIO
import RPi
import time


DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 10

in1 = 3
#in2 = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1, GPIO.OUT)
#GPIO.setup(in2, GPIO.OUT)

GPIO.output(in1, True)


fan_state = False

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    
        if humidity is not None and temperature is not None:
            print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
            # print(humidity)
        else:
            print("Failed to retrieve data from humidity sensor")

        
        if humidity >= 80:
            GPIO.output(in1,False)
            print("turning on fan")
            fan_state = True
        elif humidity <= 70 and fan_state:
            print("turning off fan")
            fan_state=False
            GPIO.output(in1,True)


        time.sleep(0.25)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("quit.")
