#!/usr/bin/env python3

import argparse
from contextlib import contextmanager


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="file to write")
    return parser.parse_args()


class Open_File:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        print("Open_File.__enter__(): opening file...")
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, traceback):
        print("Open_File.__exit__(): closing file...")
        self.file.close()


@contextmanager
def open_file(file, mode):
    try:
        print("open_file(): opening file...")
        f = open(file, mode)
        yield f
    finally:
        print("open_file(): closing file...")
        f.close()


def main():
    args = cli()
    print("\nClass implementation of context manager")
    with Open_File(args.input, "w") as f:
        print(f"Writing to {args.input}...")
        f.write("Testing")
    print(f"{args.input} closed?", f.closed)

    print("\nFunction implementation of context manager")
    with open_file(args.input, "w") as f:
        print(f"Writing to {args.input}...")
        f.write("Testing")
    print(f"{args.input} closed?", f.closed)


if __name__ == "__main__":
    main()
