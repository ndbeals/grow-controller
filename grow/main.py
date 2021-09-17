"""Loads 'logic.py' within a nice environment (with some sugar) to make setting up the logic easier."""
import devices.base

from log import log

import time

class EnvironmentDict(dict):
    # def __getattr__(self, key):
    #     if key in self:
    #         return self[key]
    #     else:
    #         raise AttributeError(key)

    # def __setattr__(self, key, value):
    #     self[key] = value
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if issubclass(type(value), devices.base.DeviceBase):
            value.name = key

def main():
    log.info("Application Starting.")

    _globals = EnvironmentDict()
    # _globals = {}
    # _locals = EnvironmentDict()

    with open('logic.py','r') as fp:
        src = fp.read()

    # time.sleep(2)
    code = compile(src, 'logic.py', 'exec' )
    exec( code , _globals )
    # exec( code , _globals, _locals )

    log.info("done.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.critical("CTRL-C caught, exiting application.")