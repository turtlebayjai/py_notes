#!/usr/bin/env python3

import argparse
import concurrent.futures
import logging
import requests
import threading
import time


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("URLs", help="URLs to download", nargs="+")
    parser.add_argument(
        "--quiet", help="only show warnings and errors", action="store_true"
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


def download_image(img_url):
    logging.info(f"Downloading from {img_url}")
    img_bytes = requests.get(img_url).content
    img_name = img_url.split("/")[-1]
    with open(img_name, "wb") as img_file:
        img_file.write(img_bytes)
        logging.info(f"{img_name} was downloaded")


@timer
def no_threading(urls):
    for url in urls:
        download_image(url)


@timer
def with_threading(urls):
    threads = []
    for url in urls:
        t = threading.Thread(target=download_image, args=[url])
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()


@timer
def with_thread_pool(urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_image, urls)


def main():
    args = cli()
    no_threading(args.URLs)
    with_threading(args.URLs)
    with_thread_pool(args.URLs)


if __name__ == "__main__":
    main()
