

class Relay():

    _gpio_pin: int
    _state: bool

    def __init__(self, gpio_pin: int):
        """
        self._state : relay state, false is off, true is on
        """
        if not gpio_pin:
            raise Exception("No GPIO Pin was provided")
        
        self._gpio_pin = gpio_pin
        self._state = False

    