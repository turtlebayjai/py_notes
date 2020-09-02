#!/usr/bin/env python3


from contextlib import contextmanager
import os


@contextmanager
def change_directory(path):
    cwd = os.getcwd()
    try:
        print("Changing directory to ", path, "...")
        os.chdir(path)
        yield
    finally:
        print("Changing directory back to ", cwd, "...")
        os.chdir(cwd)


def main():
    with change_directory("/Users/jai/Documents/CS.nosync/Python/package_tests"):
        print(os.listdir())
    print(os.listdir())


if __name__ == "__main__":
    main()
