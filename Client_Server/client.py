#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" A simple tcp client """

import sys
import os
import socket


def main():

    max_buffer = 4096

    if sys.argv < 3:
        print "\nUsage: python %s ip_addres port\n" % sys.argv[0]
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except socket.error as err_msg:
        print "[!] Socket error: %s \n" % str(err_msg[1])
        sys.exit()

    while True:
        send_msg = raw_input("-> ")
        sock.sendall(send_msg)
        recv_msg = sock.recv(max_buffer)
        print recv_msg

    sock.close()
###


if __name__ == '__main__':
    main()
