#!/usr/bin/env python3

import argparse
import time


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("seconds", help="how long to count for", type=float)
    return parser.parse_args()


def timer(time_func, seconds):
    start = time_func()
    elapsed, i = time_func() - start, 0
    while elapsed < seconds:
        i += 1
        elapsed = time_func() - start
    return (i, elapsed)


def main():
    args = cli()
    time_funcs = [time.process_time, time.perf_counter, time.time]
    for func in time_funcs:
        i, elapsed = timer(func, args.seconds)
        print(f"{func.__name__:>12}| Counted to {i:,} in {elapsed} seconds.")


if __name__ == "__main__":
    main()
