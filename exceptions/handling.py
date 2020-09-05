#!/usr/bin/env python3

import argparse
import logging


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="file to read")
    parser.add_argument("value", help="value to add one to")
    parser.add_argument(
        "-g", "--generic", help="raise generic exception", action="store_true"
    )
    logging.basicConfig(format="%(levelname)-8s | %(message)s")
    return parser.parse_args()


def main():
    args = cli()
    try:
        # Illustrative
        # Should separate possible exception events into different blocks
        f = open(args.input, "r")
        plus_one = int(args.value) + 1
        if args.generic:
            raise Exception("This is a generic exception!")
    except FileNotFoundError as e:
        logging.warning(f"{e}: this file does not exist!")
    except ValueError as e:
        logging.warning(f"{e}: {args.value} is not an int!")
        f.close()
    except Exception as e:
        # Illustrative
        # Should be as specific about exceptions as possible
        logging.error(f"{type(e).__name__}: {e.args}")
        logging.error("Something went wrong. Suspending execution.")
        f.close()
        raise e
    else:
        # Executes if no exception raised
        print(f"{args.input} contents:")
        print(f.read())
        f.close()
        print(f"{args.value} plus one:", plus_one)
    finally:
        # Executes regardless of exception raised
        print("Executing 'finally'...")

    # Continues if no exception or exception handled (not raised)
    print("main() execution continues...")


if __name__ == "__main__":
    main()
