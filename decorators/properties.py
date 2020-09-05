#!/usr/bin/env python3

import argparse
import logging


class Employee:
    def __init__(self, first, last):
        self.first = first
        self.last = last
        self.email = first + "." + last + "@email.com"

    @property
    def fullname(self):
        return f"{self.first} {self.last}"

    @property
    def property_email(self):
        return f"{self.first}.{self.last}@email.com"

    @fullname.setter
    def fullname(self, name):
        first, last = name.split(" ")
        self.first = first
        self.last = last

    @fullname.deleter
    def fullname(self):
        logging.warning(f"Deleting {self.fullname}!")
        self.first = None
        self.last = None

    def __str__(self):
        return (
            f"first: {self.first}, last: {self.last}\n"
            f"fullname: {self.fullname}\n"
            f"email: {self.email}\n"
            f"@property email: {self.property_email}"
        )

    def __repr__(self):
        return f"{self.__class__.__name__}" f"({self.first!r}, {self.last!r})"


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("first", help="first name")
    parser.add_argument("last", help="last name")
    parser.add_argument("nickname", help="nickname")
    parser.add_argument(
        "-q", "--quiet", help="only show warnings and errors", action="store_true"
    )
    args = parser.parse_args()

    format = "%(levelname)-5s | %(message)s"
    level = logging.WARNING if args.quiet else logging.INFO
    logging.basicConfig(format=format, level=level)
    return args


def main():
    args = cli()
    logging.info(f"Creating Employee('{args.first}', '{args.last}')")
    me = Employee(args.first, args.last)
    print(me)

    # Notice init email variable does not get updated
    # Should use getter/setter or property decorator
    logging.info(f"Changing first to '{args.nickname}'")
    me.first = args.nickname
    print(me)

    # Updating all connected name properties dynamically using fullname.setter
    logging.info(f"Changing fullname to '{args.first} {args.first}'")
    me.fullname = f"{args.first} {args.first}"
    print(me)

    # Deleting all connected name properties dynamically using fullname.deleter
    logging.info(f"Deleting fullname")
    del me.fullname
    print(me)


if __name__ == "__main__":
    main()
