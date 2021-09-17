import time

# import board
# import digitalio


# relay = digitalio.DigitalInOut(board.D2)
# relay.direction = digitalio.Direction.OUTPUT




import time
import gpiozero

pin = 27
# pin = "GPIO27"

# relay = gpiozero.OutputDevice(pin) #GPIO Pin #
relay = gpiozero.OutputDevice(pin,active_high=False,initial_value=True) #GPIO Pin #

# relay.off()
# relay.on()
while True:
#   print(relay.value)
#   # relay.on()
  relay.toggle()
#   print(relay.value)
  time.sleep(1)
#   for x in range(5):
#     relay.off()
#     time.sleep(4)
#     relay.on()
#     time.sleep(4)