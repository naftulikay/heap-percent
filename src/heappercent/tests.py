#!/usr/bin/env python
# -*- coding; utf-8 -*-

import os
import unittest

from heappercent import HeapSize
from heappercent.exceptions import InsufficientRamException
from heappercent.conversions import ConvertBytes, Units
from heappercent.utils import first


class UtilsTestCase(unittest.TestCase):
    """Tests utilities."""

    def test_first(self):
        """Tests that the function 'first' program does the thing."""
        self.assertEqual(0, first([0, 1, 2]))
        self.assertEqual(None, first([]))


class ConvertBytesTestCase(unittest.TestCase):
    """Test that byte conversions work properly."""

    # 1
    def test_to_bytes(self):
        """Test that converting bytes to bytes works as expected."""
        self.assertEqual(5, ConvertBytes.to_bytes(5))

    def test_from_bytes(self):
        """Test that converting bytes from bytes works as expected."""
        self.assertEqual(5, ConvertBytes.from_bytes(5))

    # 1000
    def test_to_kilobytes(self):
        """Test that converting bytes to kilobytes (1000b) works as expected."""
        self.assertEquals(4, ConvertBytes.to_kilobytes(4*1000))

    def test_from_kilobytes(self):
        """Test that converting bytes from kilobytes (1000b) to bytes works as expected."""
        self.assertEquals(4 * 1000, ConvertBytes.from_kilobytes(4))

    # 1024
    def test_to_kibibytes(self):
        """Test that converting bytes to kibibytes (1024b) works as expected."""
        self.assertEquals(4, ConvertBytes.to_kibibytes(4*1024))

    def test_from_kibibytes(self):
        """Test that converting bytes from kibibytes (1024b) to bytes works as expected."""
        self.assertEqual(4 * 1024, ConvertBytes.from_kibibytes(4))

    # 1000**2
    def test_to_megabytes(self):
        """Test converting bytes to megabytes (1000**2) works as expected."""
        self.assertEqual(4, ConvertBytes.to_megabytes(4*1000**2))

    def test_from_megabytes(self):
        """Test converting megabytes (1000**2) to bytes works as expected."""
        self.assertEqual(4 * 1000**2, ConvertBytes.from_megabytes(4))

    # 1024**2
    def test_to_mebibytes(self):
        """Tests converting bytes to mebibytes (1024**2) works as expected."""
        self.assertEqual(4, ConvertBytes.to_mebibytes(4*1024**2))

    def test_from_mebibytes(self):
        """Tests converting mebibytes (1024**2) to bytes works as expected."""
        self.assertEqual(4 * 1024**2, ConvertBytes.from_mebibytes(4))

    # 1000**3
    def test_to_gigabytes(self):
        self.assertEqual(5, ConvertBytes.to_gigabytes(5*1000**3))

    def test_from_gigabytes(self):
        self.assertEqual(3 * 1000**3, ConvertBytes.from_gigabytes(3))

    # 1024**3
    def test_to_gibibytes(self):
        self.assertEqual(8, ConvertBytes.to_gibibytes(8*1024**3))

    def test_from_gibibytes(self):
        self.assertEqual(8 * 1024**3, ConvertBytes.from_gibibytes(8))

    # 1000**4
    def test_to_terabytes(self):
        self.assertEqual(16, ConvertBytes.to_terabytes(16 * 1000**4))

    def test_from_terabytes(self):
        self.assertEqual(7 * 1000**4, ConvertBytes.from_terabytes(7))

    # 1024**4
    def test_to_tebibytes(self):
        self.assertEqual(16, ConvertBytes.to_tebibytes(16 * 1024**4))

    def test_from_tebibytes(self):
        self.assertEqual(7 * 1024**4, ConvertBytes.from_tebibytes(7))

    def test_to_formatted(self):
        self.assertEqual("4.00KiB", ConvertBytes.to_string(4096))
        self.assertEqual("4k", ConvertBytes.to_string(4096, formatstring="{number:.0f}{unit}", simple=True))
        self.assertEqual("1536m", ConvertBytes.to_string(1536*1024**2, cap=(Units.MEBIBYTE * 1).magnitude,
            formatstring="{number:.0f}{unit}", simple=True))

    def test_from_formatted(self):
        # simple cases
        self.assertEqual(4096, ConvertBytes.from_string('4096'))
        self.assertEqual(4096, ConvertBytes.from_string('4096b'))

        # base ten
        self.assertEqual(4000*1000,    ConvertBytes.from_string('4000kb'))
        self.assertEqual(4000*1000**2, ConvertBytes.from_string('4000mb'))
        self.assertEqual(4000*1000**3, ConvertBytes.from_string('4000gb'))

        # base two
        self.assertEqual(4096*1024,    ConvertBytes.from_string('4096k'))
        self.assertEqual(4096*1024,    ConvertBytes.from_string('4096kib'))
        self.assertEqual(4096*1024**2, ConvertBytes.from_string('4096m'))
        self.assertEqual(4096*1024**2, ConvertBytes.from_string('4096mib'))
        self.assertEqual(4096*1024**3, ConvertBytes.from_string('4096g'))
        self.assertEqual(4096*1024**3, ConvertBytes.from_string('4096gib'))


class HeapSizeTestCase(unittest.TestCase):

    def test_best_heap_size_min(self):
        """Test heap size calculations for minimum size."""
        min_limited_heap = HeapSize.best_heap_size(
            total_ram=6*1024**3,
            percent=50,
            min_allowed_ram=2*1024**3,
            max_allowed_ram=30*1024**3,
        )

        self.assertEqual(min_limited_heap.total, 3 * 1024**3)

    def test_best_heap_size_max(self):
        """Test best heap size calculations for limiting on maximum size regardless of percentage."""
        max_limited_heap = HeapSize.best_heap_size(
            total_ram=16 * 1024**3,
            percent=50,
            min_allowed_ram=0,
            max_allowed_ram=4 * 1024**3,
        )

        self.assertEqual(
            ConvertBytes.to_string(4 * 1024**3),
            ConvertBytes.to_string(max_limited_heap.total)
        )

    def test_best_heap_size_percentage(self):
        """Test best heap size calculations for simple percentage measurement."""
        percent_heap = HeapSize.best_heap_size(
            total_ram=8 * 1024**3,
            percent=50,
            min_allowed_ram=0,
            max_allowed_ram=32 * 1024**3
        )

        self.assertEqual(
            ConvertBytes.to_string(4 * 1024**3),
            ConvertBytes.to_string(percent_heap.total)
        )

    def test_insufficient_system_ram(self):
        """Tests that an error is thrown when there is insufficient system RAM."""
        try:
            xl_heap = HeapSize.best_heap_size(
                total_ram=16*1024**3,
                percent=90,
                min_allowed_ram=16 * 1024**3,
                max_allowed_ram=float("inf")
            )
            self.fail("Should have thrown an exception.")
        except InsufficientRamException as e:
            self.assertTrue(str(e).lower().index("system ram") >= 0)
            self.assertTrue(str(e).index("less than minimum allowed RAM") >= 0)
