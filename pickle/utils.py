#!/usr/bin/env python3

import argparse
import logging
import pickle


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--testrun", help="main() example", action="store_true")

    format = "%(levelname)-5s | %(message)s"
    logging.basicConfig(format=format, level=logging.INFO)
    return parser.parse_args()


def serialize(obj):
    pickled = pickle.dumps(obj)
    logging.info(f"Serialized {obj} to 'pickled' @ {hex(id(pickled))}")
    return pickled


def serialize_write(obj, filename):
    with open(filename, "wb") as f:
        pickle.dump(obj, f)
    logging.info(f"Serialized {obj} to '{filename}'")


def deserialize(pickled):
    obj = pickle.loads(pickled)
    logging.info(f"De-serialized {obj} from 'pickled' @ {hex(id(pickled))}")
    return obj


def deserialize_read(filename):
    with open(filename, "rb") as f:
        obj = pickle.load(f)
    logging.info(f"De-serialized {obj} from '{filename}'")
    return obj


def main():
    var = {"a": 1, "b": 2}
    filename = "test.dict"

    pickled = serialize(var)
    obj = deserialize(pickled)
    print("var == obj :", var == obj)
    # Two copies of the object
    print("var is obj :", var is obj)

    serialize_write(var, filename)
    obj = deserialize_read(filename)
    print("var == obj :", var == obj)
    # Two copies of the object
    print("var is obj :", var is obj)


if __name__ == "__main__" and cli().testrun:
    main()
