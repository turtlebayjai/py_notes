#!/usr/bin/env python3

# multiprocessing for CPU-bound tasks
# threading for IO-bound tasks

import argparse
import concurrent.futures
import logging
import multiprocessing
import time

PROCESSES = 0


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--seconds", help="how long to sleep for", required=True, type=float
    )
    parser.add_argument(
        "-p", "--processes", help="how many processes", required=True, type=int
    )
    parser.add_argument(
        "-q", "--quiet", help="only show warnings and errors", action="store_true"
    )
    args = parser.parse_args()

    format = "%(levelname)-5s | %(message)s"
    level = logging.WARNING if args.quiet else logging.INFO
    logging.basicConfig(format=format, level=level)
    return args


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        finish = time.perf_counter()
        print(f"{func.__name__} finished in {round(finish - start, 1)} seconds")

    return wrapper


def sleep_for(seconds):
    global PROCESSES
    PROCESSES += 1
    pid = PROCESSES
    print(f"sleep_for({seconds})")
    logging.info(f"pid: {pid:>2} | Sleeping for {seconds} seconds...")
    time.sleep(seconds)
    logging.info(f"pid: {pid:>2} | Done sleeping for {seconds} seconds.")
    return pid


@timer
def no_multi(seconds, processes):
    results = []
    for _ in range(processes):
        results.append(sleep_for(seconds))
        seconds += 1
    print(f"pids: {results}")


@timer
def with_multi(seconds, processes):
    asc_seconds = []
    for i in range(processes):
        asc_seconds.append(seconds + i)

    # multiprocessing.Pool handles race condition of writing to shared memory
    # But processes (as opposed to threads) create separate memory spaces
    # --> Note: logger settings & global PROCESSES (pid) not ref'd from from main or shared
    pool = multiprocessing.Pool(processes=processes)
    results = pool.map(sleep_for, asc_seconds)
    print(f"pids: {results}")


@timer
def with_multi_pool(seconds, processes):
    desc_seconds, results = [], []
    for i in range(processes - 1, -1, -1):
        desc_seconds.append(seconds + i)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        process_list = [executor.submit(sleep_for, s) for s in desc_seconds]

    for p in concurrent.futures.as_completed(process_list):
        results.append(p.result())
    print(f"pids: {results}")


def main():
    args = cli()
    no_multi(args.seconds, args.processes)
    with_multi(args.seconds, args.processes)
    with_multi_pool(args.seconds, args.processes)


if __name__ == "__main__":
    main()
