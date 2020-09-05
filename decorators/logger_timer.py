#!/usr/bin/env python3

import argparse
import logging
import time


""" Output from 'logger_timer.py 3':
my_timer      | Initializing my_timer
my_timer      | Returning from my_timer
my_logger     | Initializing my_logger
my_logger     | Returning from my_logger
logger_wrapper| Running timer_wrapper with args: (3,), and kwargs: {}
timer_wrapper | Running sleep_for with args: (3,), and kwargs: {}
sleep_for     | Sleeping for 3 secs...
sleep_for     | I'm awake now.
sleep_for     | Returning 'This message was returned by sleep_for -> timer_wrapper -> logger_wrapper -> main'
timer_wrapper | sleep_for ran in: 3.001495122909546 secs
timer_wrapper | Returning 'This message was returned by sleep_for -> timer_wrapper -> logger_wrapper -> main'
logger_wrapper| Closing log
logger_wrapper| Returning 'This message was returned by sleep_for -> timer_wrapper -> logger_wrapper -> main'
__main__      | This message was returned by sleep_for -> timer_wrapper -> logger_wrapper -> main
"""


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("secs", help="time to sleep", type=int)
    return parser.parse_args()


def my_logger(orig_func):
    print(f"{my_logger.__name__:14}| Initializing my_logger")
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    def logger_wrapper(*args, **kwargs):
        logging.info(
            f"{logger_wrapper.__name__:14}| Running {orig_func.__name__} with args: {args}, and kwargs: {kwargs}"
        )
        result = orig_func(*args, **kwargs)
        logging.info(f"{logger_wrapper.__name__:14}| Closing log")
        logging.info(f"{logger_wrapper.__name__:14}| Returning '{result}'")
        return result

    logging.info(f"{my_logger.__name__:14}| Returning from my_logger")
    return logger_wrapper


def my_timer(orig_func):
    print(f"{my_timer.__name__:14}| Initializing my_timer")

    def timer_wrapper(*args, **kwargs):
        print(
            f"{timer_wrapper.__name__:14}| Running {orig_func.__name__} with args: {args}, and kwargs: {kwargs}"
        )
        start = time.time()
        result = orig_func(*args, **kwargs)
        elapsed = time.time() - start
        print(
            f"{timer_wrapper.__name__:14}| {orig_func.__name__} ran in: {elapsed} secs"
        )
        print(f"{timer_wrapper.__name__:14}| Returning '{result}'")
        return result

    print(f"{my_timer.__name__:14}| Returning from my_timer")
    return timer_wrapper


# Notice my_timer is both initialized and torn down before my_logger
# However logger_wrapper calls timer_wrapper which calls sleep_for
@my_logger
@my_timer
def sleep_for(secs):
    function = "sleep_for"
    print(f"{function:14}| Sleeping for {secs} secs...")
    time.sleep(secs)
    print(f"{function:14}| I'm awake now.")
    result = "This message was returned by sleep_for -> timer_wrapper -> logger_wrapper -> main"
    print(f"{function:14}| Returning '{result}'")
    return result


def main():
    args = cli()
    result = sleep_for(args.secs)
    print(f"{__name__:14}| {result}")


if __name__ == "__main__":
    main()
