#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    An ftp scanner.
"""

import sys
import signal
import argparse
import ipaddress
from termcolor import colored


# Signal handler
def sig_handler(signum, frame):
    """"Signal handler function."""
    print("\nCaught Ctrl/C signal!")
    print("Bye bye ...")
###


# Main function
def main():
    """MAIN function."""

    __version__ = 'v0.1'

    # Signal SIGINT
    signal.signal(signal.SIGINT, sig_handler)

    # Argument parser
    parser = argparse.ArgumentParser(description="A service bot!",
                                     usage="%(prog)s [options] ip-range",
                                     epilog="<*> Happy scan! <*>\n")
    parser.add_argument("ip_range", metavar='IP', help="ip range.")
    parser.add_argument("-p", "--port", help="Set non standard port.")
    parser.add_argument('--version', action='version', version=__version__)
    args = parser.parse_args()

    text = colored("<*> Program starting...", 'green')
    print(text)

    net4 = ipaddress.ip_network(args.ip_range)
    for x in net4.hosts():
        print(x)
###


if __name__ == '__main__':
    main()
