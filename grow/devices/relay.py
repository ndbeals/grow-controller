
import gpiozero

from devices.base import OutputBase
# from outputs import OutputBase


# class Relay(gpiozero.OutputDevice, OutputBase):
class Relay(OutputBase, gpiozero.OutputDevice):
    pass
    # def __init__(self, **kwargs) -> None:
    #     print("relay init",kwargs)

    #     super().__init__( **kwargs )
    #     # super(Relay,self).__init__(pin,active_high=False,initial_value=True)
    #     # super().__init__(pin,active_high=False,initial_value=True)
    #     # super().__init__()