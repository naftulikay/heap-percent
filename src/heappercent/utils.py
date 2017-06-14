#!/usr/bin/env python
# -*- coding: utf-8 -*-


def first(sequence):
    """Returns the first item in a non-empty sequence, otherwise None."""
    return sequence[0] if len(sequence) > 0 else None
