#!/usr/bin/env python3

import argparse
from contextlib import contextmanager
import os


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="list files in path")
    return parser.parse_args()


@contextmanager
def change_directory(path):
    cwd = os.getcwd()
    try:
        print(f"Changing directory to {path}...")
        os.chdir(path)
        yield
    finally:
        print(f"Changing directory back to {cwd}...")
        os.chdir(cwd)


def main():
    args = cli()
    with change_directory(args.path):
        print(os.listdir())
    # Back in original directory
    print(os.listdir())


if __name__ == "__main__":
    main()
