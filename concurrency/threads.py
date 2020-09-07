#!/usr/bin/env python3

# threading for IO-bound processes
# multiprocessing for CPU-bond processes (parallelism)
import argparse
import concurrent.futures
import logging
import threading
import time

PROCESSES = 0


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--seconds", help="how long to sleep for", required=True, type=float
    )
    parser.add_argument(
        "-t", "--threads", help="number of threads", required=True, type=int
    )
    parser.add_argument(
        "-q", "--quiet", help="only show warnings and errors", action="store_true"
    )
    args = parser.parse_args()

    format = "%(levelname)-5s| %(message)s"
    level = logging.WARNING if args.quiet else logging.INFO
    logging.basicConfig(format=format, level=level)
    return args


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        finish = time.perf_counter()
        print(f"{func.__name__}: finished in {finish - start:.1f} seconds")
        return result

    return wrapper


def sleep_for(seconds):
    global PROCESSES
    PROCESSES += 1
    pid = PROCESSES
    logging.info(f"pid:{pid:>3}| Sleeping for {seconds} seconds...")
    time.sleep(seconds)
    logging.info(f"pid:{pid:>3}| Done sleeping for {seconds} seconds")
    return pid


@timer
def no_threading(seconds, n_calls):
    results = []
    for _ in range(n_calls):
        results.append(sleep_for(seconds))
        seconds += 1
    print(f"pid in order of completion: {results}")


@timer
def with_threading(seconds, n_threads):
    # Use a lambda function and mutable strcture to access threads' return values
    thread_list, results = [], []
    for _ in range(n_threads):
        t = threading.Thread(
            target=lambda l, s: l.append(sleep_for(s)), args=[results, seconds]
        )
        t.start()
        # join() blocks main() execution until the 'joined' thread terminates
        # Calling join() now will stop further loop execution
        thread_list.append(t)
        seconds += 1
    # Call join() after starting all threads (will wait for thread to finish)
    # Notice: did not join() last thread, so finishes after main() continues
    for thread in thread_list[:-1]:
        thread.join()
    # Last thread will not appear in results (still executing).
    print(f"pid in order of completion: {results}")


@timer
def with_thread_pool(seconds, n_threads):
    # Initialize ThreadPoolExecutor()
    # Kickoff thread using submit() (save reference to get result later)
    # Get result using result() (main() execution suspended for threads in context manager)
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        desc_seconds = []
        for i in range(n_threads - 1, -1, -1):
            desc_seconds.append(seconds + i)
        thread_list = [executor.submit(sleep_for, s) for s in desc_seconds]
        """
        # Appends in thread_list order regardless of completion
        for thread in thread_list:
            results.append(thread.result())
        print(f"pid in order of thread_list: {results}")
        """
        # Appends in order of completion regardless of thread_list order
        for thread in concurrent.futures.as_completed(thread_list):
            results.append(thread.result())
        print(f"pid in order of completion: {results}")


def main():
    args = cli()
    no_threading(args.seconds, args.threads)
    with_threading(args.seconds, args.threads)
    with_thread_pool(args.seconds, args.threads)


if __name__ == "__main__":
    main()
