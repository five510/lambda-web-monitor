import time
import re
import logging
from functools import wraps
log_handler = {}

def get_logger(log_name='default'):

    #Add stdout handler
    global log_handler
    if log_name not in log_handler:
        formatter = logging.Formatter("[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s")
        log_handler[log_name] = logging.StreamHandler()
        log_handler[log_name].setFormatter(formatter)
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler[log_name])
    return logger

def logging_handler(func):
    logger = get_logger()
    def wrapper(event, context):
        logger.info(event)
        try:
            ret = func(event, context)
            logger.info(ret)
        except Exception as e:
            logger.exception(str(e))
            raise e
        return ret
    return wrapper

def watch_time(func):
    logger = get_logger()
    @wraps(func)
    def wrapper(*args, **kargs):
        start = time.time()
        result = func(*args,**kargs)
        process_time =  time.time() - start
        logger.info(f"Process time of {func.__name__} is {process_time} ")
        return result
    return wrapper