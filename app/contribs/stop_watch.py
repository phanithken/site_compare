import time
from functools import wraps


def stop_watch(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        start = time.time()
        result = func(*args, **kargs)
        elapsed_time = time.time() - start
        print("##STOP_WATCH## {} : {:.4f} sec".format(
            func.__name__.ljust(30), elapsed_time))
        return result

    return wrapper