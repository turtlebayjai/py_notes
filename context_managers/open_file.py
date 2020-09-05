#!/usr/bin/env python3

import argparse
from contextlib import contextmanager
import logging


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="file to write")
    parser.add_argument(
        "-q", "--quiet", help="only show warnings and errors", action="store_true"
    )
    args = parser.parse_args()

    format = "%(levelname)-5s | %(message)s"
    level = logging.WARNING if args.quiet else logging.INFO
    logging.basicConfig(format=format, level=level)
    return args


class Open_File:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        logging.info("Open_File.__enter__(): opening file...")
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, traceback):
        logging.info("Open_File.__exit__(): closing file...")
        self.file.close()


@contextmanager
def open_file(file, mode):
    try:
        logging.info("open_file(): opening file...")
        f = open(file, mode)
        yield f
    finally:
        logging.info("open_file(): closing file...")
        f.close()


def main():
    args = cli()

    # Class implementation of context manager
    with Open_File(args.input, "w") as f:
        logging.info(f"Writing to {args.input}...")
        f.write("Testing")
    print(f"{args.input} closed?", f.closed)

    # Function implementation of context manager
    with open_file(args.input, "w") as f:
        logging.info(f"Writing to {args.input}...")
        f.write("Testing")
    print(f"{args.input} closed?", f.closed)


if __name__ == "__main__":
    main()
