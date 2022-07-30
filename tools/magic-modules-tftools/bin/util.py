import logging
from time import time

from termcolor import colored


def show_warning(text):
    print(colored(color="red", text=str(text + "\n")))


def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        line = "---------------------[starting - {}]---------------------"
        logging.debug(line.format(func.__name__))
        result = func(*args, **kwargs)
        t2 = time()
        logging.info(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s")
        line = "---------------------[ending - {}]---------------------"
        return result

    return wrap_func
