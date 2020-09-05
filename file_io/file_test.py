#!/usr/bin/env python3

import argparse
import logging


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="file to be copied")
    parser.add_argument("output", help="file to be written")
    parser.add_argument("chunk", help="chunk size", type=int)
    parser.add_argument(
        "-q", "--quiet", help="only print warnings and errors", action="store_true"
    )
    args = parser.parse_args()

    format = "%(levelname)-5s | %(message)s"
    level = logging.INFO if not args.quiet else None
    logging.basicConfig(format=format, level=level)
    return args


def print_msg(func):
    def wrapper(*args, **kwargs):
        logging.info(f"{func.__name__}{args}...")
        func(*args, **kwargs)
        logging.info(f"'{args[0]}' copied to '{args[1]}'")

    return wrapper


@print_msg
def copy_text_file(input_path, output_path):
    with open(input_path, "r") as rf, open(output_path, "w") as wf:
        for line in rf:
            wf.write(line)


@print_msg
def copy_text_chunks(input_path, output_path, chunk_size):
    with open(input_path, "r") as rf, open(output_path, "w") as wf:
        rf_chunk = rf.read(chunk_size)
        while len(rf_chunk) > 0:
            wf.write(rf_chunk)
            rf_chunk = rf.read(chunk_size)


@print_msg
def copy_bytes(input_path, output_path):
    # Use 'rb' and 'wb' to read/write bytes
    # Works for all file formats (txt, jpg, etc)
    with open(input_path, "rb") as rf, open(output_path, "wb") as wf:
        for line in rf:
            wf.write(line)


def main():
    args = cli()
    try:
        copy_text_file(args.input, args.output)
        copy_text_chunks(args.input, args.output, args.chunk)
    except UnicodeDecodeError as e:
        logging.error(f"{type(e).__name__}: {e}")
        logging.error(f"{args.input} file type unsupported")
        logging.error("skipping copy_text_file() and copy_text_chunks()")
    copy_bytes(args.input, args.output)


if __name__ == "__main__":
    main()
