#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    An ftp scanner.
"""

import sys
import signal


# Signal handler
def sig_handler(signum, frame):
    """"Signal handler function."""
    print("\nCaught Ctrl/C signal!")
    print("Bye bye ...")
###


# Main function
def main():
    """MAIN function."""

    # Signal SIGINT
    signal.signal(signal.SIGINT, sig_handler)
###


if __name__ == '__main__':
    main()
