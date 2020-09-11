#!/usr/bin/env python3

import argparse
import logging
import pickle
import socket

HEADER_SIZE = 20


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("IPv4", help="IPv4 address to bind")
    parser.add_argument("PORT", help="port number to bind", type=int)
    parser.add_argument(
        "-q", "--quiet", help="only show warnings and errors", action="store_true"
    )
    args = parser.parse_args()

    format = "%(levelname)-5s | %(message)s"
    level = logging.WARNING if args.quiet else logging.INFO
    logging.basicConfig(format=format, level=level)
    return args


def send_msg(sock, obj):
    ser_obj = pickle.dumps(obj)
    header = f"{len(ser_obj): <{HEADER_SIZE}}"
    full_msg = bytes(header, "utf-8") + ser_obj
    sock.send(full_msg)


def main():
    args = cli()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address_port = (args.IPv4, args.PORT)
    logging.info(f"Binding socket to {address_port}...")
    s.bind(address_port)
    logging.info(f"Server is listening...")
    s.listen()

    while True:
        client_socket, address = s.accept()
        logging.info(f"Connection from {address} established!")
        send_msg(client_socket, f"Connection to {address_port} established!")

        prompt = f"send to {address[0]}:{address[1]} > "
        msg = input(prompt)
        while msg.lower() != "close":
            send_msg(client_socket, msg)
            msg = input(prompt)
        client_socket.close()


if __name__ == "__main__":
    main()
