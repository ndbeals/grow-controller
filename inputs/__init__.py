from .base import InputBase

RegisteredDevices = InputBase.RegisteredDevices


def _load_devices():
    import importlib
    from pathlib import Path

    _ignored_names = ("base.py","__init__.py")
    _here = Path(__file__).parent.resolve()

    for module in _here.glob('*.py'):
        if module.is_file() and not module.name in _ignored_names:
            # print("loading ",module)
            importlib.import_module(f'{__package__}.{module.name[:-3]}')
            # pass
            # loaded = importlib.import_module(f'{__package__}.{module.name[:-3]}')

            # _InputDevices.append(loaded)

_load_devices()
