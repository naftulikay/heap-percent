#!/usr/bin/env python
# -*- coding; utf-8 -*-

from __future__ import print_function

from heappercent.conversions import ConvertBytes, Units
from heappercent.exceptions import ConversionException, InsufficientRamException
from heappercent.utils import first

from math import floor

import argparse
import json
import psutil
import re
import sys


class HeapSize(object):

    @classmethod
    def best_heap_size(cls, total_ram, percent, min_allowed_ram, max_allowed_ram):
        # do math right; multiply total ram in bytes by the percentage (limited to 1-100) multiplied by 0.01 to shift
        ideal_size = int(total_ram * float(max(1, min(100, percent)) * 0.01))

        if min_allowed_ram >= total_ram:
            min_allowed_gb, total_ram_gb = (((Units.BYTE * min_allowed_ram) / (Units.GIBIBYTE * 1))).magnitude, \
                ((Units.BYTE * total_ram) / (Units.GIBIBYTE * 1)).magnitude
            raise InsufficientRamException("System RAM ({:02.02f}GiB) is less than minimum allowed RAM ({:02.02f}GiB)"
                .format(total_ram_gb, min_allowed_gb))

        return HeapSize(min(max(ideal_size, min_allowed_ram), max_allowed_ram))

    def __init__(self, in_bytes):
        self._total = in_bytes

    def __eq__(self, other):
        if not isinstance(other, HeapSize) and isinstance(other, (int, float)):
            other = HeapSize(other)

        return self._total == other.total

    def __str__(self):
        return ""

    def __repr__(self):
        return "{d}".format(self.total)

    @property
    def size(self):
        return self._total

    @property
    def total(self):
        return self._total


def main():
    """Main entrypoint."""
    parser = argparse.ArgumentParser(
        description='delivers the calculated amount of ram to use for a process',
        epilog='sizes may be integers in bytes, or may have the following case-insensitive suffixes for size: b, k, kb, kib,' \
               'm, mb, mib, g, gb, gib, t, tb, tib.'
    )

    parser.add_argument('--min', '--min-allowed-ram', default='2GiB', type=str,
        help="The minimum allowed RAM for the process; defaults to 2GiB, set to zero if you want it to run no matter "
             "what.")
    parser.add_argument('--max', '--max-allowed-ram', default='30GiB', type=str,
        help="The maximum allowed RAM for the process; defaults to 30GiB, set to a very high number if you don't care "
             "about maximum heap size, ie 100TiB.")
    parser.add_argument('-t', '--total', type=str, required=False, default=None,
        help="The total system RAM; will be detected if not set.")

    parser.add_argument('-p', '--percent', type=float, required=True, help="The RAM percentage to attempt to occupy.")

    args = parser.parse_args()

    try:
        # determine input min/max allowed RAM by converting strings to byte counts
        min_allowed_ram = ConvertBytes.from_string(args.min)
        max_allowed_ram = ConvertBytes.from_string(args.max)
        # learn the total memory unless otherwise specified
        total_ram = ConvertBytes.from_string(args.total) if args.total else psutil.virtual_memory().total
    except ConversionException as e:
        fail(str(e), rc=1)

    try:
        heap_size = HeapSize.best_heap_size(
            total_ram=total_ram,
            percent=args.percent,
            min_allowed_ram=min_allowed_ram,
            max_allowed_ram=max_allowed_ram
        )

        print(
            ConvertBytes.to_string(heap_size.size, cap=((Units.MEBIBYTE * 1).to(Units.BYTE)).magnitude, simple=True,
                formatstring="{number:.0f}{unit}")
        )

    except InsufficientRamException as e:
        fail(str(e), rc=2)


def fail(message, *args, **kwargs):
    rc = first(list(
        filter(lambda i: i != None,
            [(kwargs or {}).get(key, None) for key in ('rc', 'returncode')]
        )
    )) or 1

    sys.stderr.write("ERROR: {}\n".format(message.format(*args)))
    sys.stderr.flush()
    sys.exit(rc)


if __name__ == "__main__":
    main()
