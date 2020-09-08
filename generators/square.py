#!/usr/bin/env python3

import argparse
import logging


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("nums", help="numbers to square", nargs="+", type=float)
    parser.add_argument(
        "-q", "--quiet", help="only show warnings and errors", action="store_true"
    )
    args = parser.parse_args()

    format = "%(levelname)-5s | %(message)s"
    level = logging.WARNING if args.quiet else logging.INFO
    logging.basicConfig(format=format, level=level)
    return args


def square_nums(nums):
    for num in nums:
        yield num * num


def square_comprehension(nums):
    return (num * num for num in nums)


def print_gen_vals(generator):
    # One at a time
    print(next(generator))
    # Or loop
    for num in generator:
        print(num)


def main():
    args = cli()
    # Generator object: all results not stored in memory
    my_nums = square_nums(args.nums)
    logging.info(f"my_nums: {my_nums}")
    print_gen_vals(my_nums)

    my_nums = square_comprehension(args.nums)
    logging.info(f"my_nums: {my_nums}")
    print_gen_vals(my_nums)


if __name__ == "__main__":
    main()
