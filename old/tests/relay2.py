import time

import board
import digitalio


relay = digitalio.DigitalInOut(board.D2)
relay.direction = digitalio.Direction.OUTPUT



# try:
while True:
  for x in range(5):
          # GPIO.output(in1, True)
          relay.value = True
          time.sleep(4)
          relay.value = False
          # GPIO.output(in1, False)
#           GPIO.output(in2, True)
          time.sleep(4)