#!/usr/bin/env python3
"""Dump the lexer tags.
This is used for testing.
"""
import sys
import argparse
from beancount.parser import parser


def main():
    parser = argparse.ArgumentParser(__doc__.strip())
    parser.add_argument('filename', help='Beancount input filename.')
    opts = parser.parse_args()

    parser.dump_lexer(opts.filename, sys.stdout)


if __name__ == '__main__':
    main()
