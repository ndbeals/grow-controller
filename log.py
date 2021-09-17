import sys

from loguru import logger
log = logger
# <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>
# default format for loguru

# logger.remove(0) # Remove default logger (level="DEBUG")
# logger.add(sys.stderr,level="TRACE") # re add default logged but level="TRACE"

# logger.level("test",no=1)

# def filt(*args,**kwargs):
#     print(args,kwargs)

# logger.add(sys.stderr, format="custom add {level} {message}", level="test", filter=filt)
# logger.add(sys.stderr, format="custom add {level} {message}", level="test", filter={'str':'test'})
# logger.add(sys.stderr, format="custom add {level} {message}", level="test", filter="__main__")


# logger.add("test_{time}.log",colorize=True)

# logger.log("test","hiiiiiiii")

# logger.trace("trace")
# logger.debug("debug")
# logger.info("info")
# logger.success("success")
# logger.warning("warning")
# logger.error("error")
# logger.critical("critical")