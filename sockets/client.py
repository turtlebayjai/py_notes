#!/usr/bin/env python3

import argparse
import logging
import pickle
import socket


HEADER_SIZE = 20


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("IPv4", help="IPv4 address to connect to")
    parser.add_argument("PORT", help="port number to connect to", type=int)
    parser.add_argument(
        "-b", "--buffer", help="buffer size (bytes)", default=8, type=int
    )
    parser.add_argument(
        "-q", "--quiet", help="only show warnings and errors", action="store_true"
    )
    args = parser.parse_args()

    format = "%(levelname)-5s | %(message)s"
    level = logging.WARNING if args.quiet else logging.INFO
    logging.basicConfig(format=format, level=level)
    return args


def read_msg(sock, buffer_size):
    print(f"buffer: {buffer_size}")
    header = sock.recv(HEADER_SIZE)
    msg_len = int(header.decode("utf-8"))

    msg = b""
    while len(msg) < msg_len:
        bytes_to_read = min(buffer_size, msg_len - len(msg))
        msg += sock.recv(bytes_to_read)
    return pickle.loads(msg)


def main():
    args = cli()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address_port = (args.IPv4, args.PORT)
    logging.info(f"Connecting to {address_port}...")
    s.connect(address_port)

    while True:
        try:
            msg = read_msg(s, args.buffer)
        except:
            break
        else:
            print(msg)


if __name__ == "__main__":
    main()
