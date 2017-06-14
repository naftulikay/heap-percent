#!/usr/bin/env python
# -*- coding: utf-8 -*-

from heappercent.utils import first

from pint import UnitRegistry

import os, re


class Registry(object):

    __registry = UnitRegistry(os.path.join(os.path.dirname(__file__), "fixtures", "default_en.txt"))

    @classmethod
    def get(cls):
        return cls.__registry

class Units(object):

    BYTE     = (1 * Registry.get().byte).to(Registry.get().byte)
    KIBIBYTE = (1 * Registry.get().kibibyte).to(Registry.get().byte)
    KILOBYTE = (1 * Registry.get().kilobyte).to(Registry.get().byte)
    MEBIBYTE = (1 * Registry.get().mebibyte).to(Registry.get().byte)
    MEGABYTE = (1 * Registry.get().megabyte).to(Registry.get().byte)
    GIGABYTE = (1 * Registry.get().gigabyte).to(Registry.get().byte)
    GIBIBYTE = (1 * Registry.get().gibibyte).to(Registry.get().byte)
    TERABYTE = (1 * Registry.get().terabyte).to(Registry.get().byte)
    TEBIBYTE = (1 * Registry.get().tebibyte).to(Registry.get().byte)


class ConvertBytes(object):

    ALLOWED_UNITS = ('b', 'k', 'kb', 'kib', 'm', 'mb', 'mib', 'g', 'gb', 'gib', 't', 'tb', 'tib')

    SIZE_FORMAT = re.compile(r"""
        (?<=\b)
        (?P<number>
            (?P<integer>\d+)
            (?:\.
                (?P<decimal>\d+)
            )?
        )
        \s*
        (?P<mod>
            (?:b|k|ki?b|m|mi?b|g|gi?b|t|ti?b)?
        )
        (?=\b)
    """.strip(), re.X | re.I)

    __FROM_MAPPINGS = {}

    @classmethod
    def get_from_mappings(cls):
        if len(cls.__FROM_MAPPINGS.keys()) == 0:
            cls.__FROM_MAPPINGS.update({
                ('b',):      cls.from_bytes,
                ('kb',):     cls.from_kilobytes,
                ('k','kib'): cls.from_kibibytes,
                ('mb',):     cls.from_megabytes,
                ('m','mib'): cls.from_mebibytes,
                ('gb',):     cls.from_gigabytes,
                ('g','gib'): cls.from_gibibytes,
                ('tb',):     cls.from_terabytes,
                ('t','tib'): cls.from_tebibytes
            })

        return cls.__FROM_MAPPINGS

    @classmethod
    def get_to_mappings(cls):
        if len(cls.__TO_MAPPINGS.keys()) == 0:
            cls.__TO_MAPPINGS.update({
                ('b',):      cls.to_bytes,
                ('kb',):     cls.to_kilobytes,
                ('k','kib'): cls.to_kibibytes,
                ('mb',):     cls.to_megabytes,
                ('m','mib'): cls.to_mebibytes,
                ('gb',):     cls.to_gigabytes,
                ('g','gib'): cls.to_gibibytes,
                ('tb',):     cls.to_terabytes,
                ('t','tib'): cls.to_tebibytes
            })

        return cls.__TO_MAPPINGS

    @classmethod
    def from_string(cls, value):
        """Converts a string into integer of bytes."""
        m = cls.SIZE_FORMAT.search(value)

        if not m:
            raise ConversionException("unable to detect size from \"{}\"".format(value))

        mod = (m.group('mod') or 'b').lower()

        if not mod in cls.ALLOWED_UNITS:
            raise ConversionException("unable to detect size modifier \"{}\"".format(mod))

        number = float(m.group('number')) if mod != 'b' else int(m.group('number'))

        key = first([keygroup for keygroup in cls.get_from_mappings().keys() if mod in keygroup])

        return int(round(cls.get_from_mappings()[key](number))) if key else None

    @classmethod
    def to_string(cls, byte_count, cap=float('inf'), simple=False, formatstring="{number:.2f}{unit}"):
        mod = 'b'
        divisor = 1

        if byte_count >= Units.KIBIBYTE and cap >= Units.KIBIBYTE:
            mod, divisor = 'KiB' if not simple else 'k', 1024

        if byte_count >= Units.MEBIBYTE and cap >= Units.MEBIBYTE:
            mod, divisor = 'MiB' if not simple else 'm', 1024**2

        if byte_count >= Units.GIBIBYTE and cap >= Units.GIBIBYTE:
            mod, divisor = 'GiB' if not simple else 'g', 1024**3

        if byte_count >= Units.TEBIBYTE and cap >= Units.TEBIBYTE:
            mod, divisor = 'TiB' if not simple else 't', 1024**4

        return formatstring.format(number=byte_count/divisor, unit=mod)

    # 1
    @classmethod
    def to_bytes(cls, byte_count):
        return byte_count

    @classmethod
    def from_bytes(cls, byte_count):
        return byte_count

    # 1000
    @classmethod
    def to_kilobytes(cls, byte_count):
        return (byte_count / Units.KILOBYTE.to(Units.BYTE)).magnitude

    @classmethod
    def from_kilobytes(cls, kb_count):
        return (kb_count * Units.KILOBYTE.to(Units.BYTE)).magnitude

    # 1024
    @classmethod
    def to_kibibytes(cls, byte_count):
        return (byte_count / Units.KIBIBYTE.to(Units.BYTE)).magnitude

    @classmethod
    def from_kibibytes(cls, byte_count):
        return (byte_count * Units.KIBIBYTE.to(Units.BYTE)).magnitude

    # 1000**2
    @classmethod
    def to_megabytes(cls, byte_count):
        return (byte_count / Units.MEGABYTE.to(Units.BYTE)).magnitude

    @classmethod
    def from_megabytes(cls, mb_count):
        return (mb_count * Units.MEGABYTE.to(Units.BYTE)).magnitude

    # 1024**2
    @classmethod
    def to_mebibytes(cls, byte_count):
        return (byte_count / Units.MEBIBYTE.to(Units.BYTE)).magnitude

    @classmethod
    def from_mebibytes(cls, mib_count):
        return mib_count * Units.MEBIBYTE.to(Units.BYTE).magnitude

    # 1000**3
    @classmethod
    def to_gigabytes(cls, byte_count):
        return (byte_count / Units.GIGABYTE.to(Units.BYTE)).magnitude

    @classmethod
    def from_gigabytes(cls, gb_count):
        return (gb_count * Units.GIGABYTE.to(Units.BYTE)).magnitude

    # 1024**3
    @classmethod
    def to_gibibytes(cls, byte_count):
        return (byte_count / Units.GIBIBYTE.to(Units.BYTE)).magnitude

    @classmethod
    def from_gibibytes(cls, gib_count):
        return (gib_count * Units.GIBIBYTE.to(Units.BYTE)).magnitude

    # 1000**4
    @classmethod
    def to_terabytes(cls, byte_count):
        return (byte_count / Units.TERABYTE.to(Units.BYTE)).magnitude

    @classmethod
    def from_terabytes(cls, count):
        return (count * Units.TERABYTE.to(Units.BYTE)).magnitude

    # 1024**4
    @classmethod
    def to_tebibytes(cls, byte_count):
        return (byte_count / Units.TEBIBYTE.to(Units.BYTE)).magnitude

    @classmethod
    def from_tebibytes(cls, count):
        return (count * Units.TEBIBYTE.to(Units.BYTE)).magnitude
