#!/usr/bin/env python3

import logging
import time


def my_logger(orig_func):
    logging.basicConfig(level=logging.INFO)

    def wrapper(*args, **kwargs):
        logging.info(f"Ran with args: {args}, and kwargs: {kwargs}")
        return orig_func(*args, **kwargs)

    return wrapper


def my_timer(orig_func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_func(*args, **kwargs)
        t2 = time.time() - t1
        print(f"{orig_func.__name__} ran in: {t2} sec")
        return result

    return wrapper


@my_logger
@my_timer
def display_info(name, age):
    print(f"display_info ran with arguments ({name}, {age})")


def main():
    display_info("Jai", 29)


if __name__ == "__main__":
    main()
