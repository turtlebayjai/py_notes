#!/usr/bin/env python3

import argparse
import concurrent.futures
import logging
import os
import requests
import threading
import time


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URLs to download", nargs="+")
    parser.add_argument("-f", "--file", help="File containing URLs")
    parser.add_argument("-d", "--dir", help="Directory to save to", default="")
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


def download(url, dir=""):
    logging.info(f"Downloading from {url}")
    url_bytes = requests.get(url).content
    url_name = url.split("/")[-1] if url.split("/")[-1] else url.split("/")[-2]
    with open(os.path.join(dir, url_name), "wb") as f:
        f.write(url_bytes)
        logging.info(f"{url_name} was downloaded")


@timer
def no_threading(urls, dir):
    for url in urls:
        download(url, dir)


@timer
def with_threading(urls, dir):
    threads = []
    for url in urls:
        t = threading.Thread(target=download, args=[url, dir])
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()


@timer
def with_thread_pool(urls, dir):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download, urls, [dir] * len(urls))


def main():
    args = cli()
    urls = args.url
    urls_file = args.file

    url_list = []
    if urls:
        url_list += urls
    if urls_file:
        with open(urls_file, "r") as f:
            url_list += [url for url in f.read().split("\n") if url]

    no_threading(url_list, args.dir)
    with_threading(url_list, args.dir)
    with_thread_pool(url_list, args.dir)


if __name__ == "__main__":
    main()
