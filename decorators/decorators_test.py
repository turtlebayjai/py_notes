#!/usr/bin/env python3


def my_logger(orig_func):
    import logging
    logging.basicConfig(level=logging.INFO)

    def wrapper(*args, **kwargs):
        logging.info("Ran with args: {}, and kwargs: {}".format(args, kwargs))
        return orig_func(*args, **kwargs)

    return wrapper


def my_timer(orig_func):
    import time

    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_func(*args, **kwargs)
        t2 = time.time() - t1
        print("{} ran in: {} sec".format(orig_func.__name__, t2))
        return result

    return wrapper


@my_logger
@my_timer
def display_info(name, age):
    print("display_info ran with arguments ({}, {})".format(name, age))


def main():
    display_info("Jai", 29)


if __name__ == "__main__":
    main()
