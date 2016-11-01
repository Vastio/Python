#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    An ftp scanner.
"""

import sys
import signal
import argparse


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
                                     epilog="Happy scan!")
    parser.add_argument("ip-range", metavar='IP', help="ip range.")
    parser.add_argument("-p", "--port", help="Set non standard port.")
    parser.add_argument('--version', action='version', version=__version__)
    args = parser.parse_args()

###


if __name__ == '__main__':
    main()
