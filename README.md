# heap-percent [![Build Status][svg-travis]][travis]

A utility for calculating the maximum heap size by system RAM, an absolute minimum RAM needed, and a maximum heap size
to not exceed. The algorithm in its entirety, operating on bytes, looks like this:

```python
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
```

Essentially, this allows to set a cap on the high heap size so as to avoid larger pointer memory space, allows to
set a cap on minimum RAM that the application _must_ have, and allows specifying a percentage to determine how much
of system RAM (capped at the max) should be dedicated to the heap of a given (typically JVM) process.

## Usage

Command-line usage:

```
usage: heap-percent [-h] [--min MIN] [--max MAX] [-t TOTAL] -p PERCENT

delivers the calculated amount of ram to use for a process

optional arguments:
  -h, --help            show this help message and exit
  --min MIN, --min-allowed-ram MIN
                        The minimum allowed RAM for the process; defaults to
                        2GiB, set to zero if you want it to run no matter
                        what.
  --max MAX, --max-allowed-ram MAX
                        The maximum allowed RAM for the process; defaults to
                        30GiB, set to a very high number if you don't care
                        about maximum heap size, ie 100TiB.
  -t TOTAL, --total TOTAL
                        The total system RAM; will be detected if not set.
  -p PERCENT, --percent PERCENT
                        The RAM percentage to attempt to occupy.

sizes may be integers in bytes, or may have the following case-insensitive
suffixes for size: b, k, kb, kib,m, mb, mib, g, gb, gib, t, tb, tib.
```

If an impossible situation arises, the error will be logged to standard output and the process will exit with a return
code of 2. Basically, this can only happen in the following cases:

 1. Your system RAM is less than your `--min` allowed RAM.
 1. Your ideal heap size is less than your `--min` allowed RAM. This can happen when the total system RAM divided by
    `--percent` is less than `--min` allowed RAM.

### From the Trenches

Try to occupy 90% of system RAM, with a minimum heap size of 5GiB.:

```
[vagrant@devel vagrant]$ bin/heap-percent --min 5GiB -p 90
ERROR: System RAM (0.97GiB) is less than minimum allowed RAM (5.00GiB)
[vagrant@devel vagrant]$ echo $?
2
```

Try to occupy 60% of specified total system RAM, being 64 GiB, with a minimum size of 2 GiB and a maximum size of 30
GiB:

```
[vagrant@devel vagrant]$ bin/heap-percent --min 2GiB --max 30GiB --total 64GiB --percent 60
30720m
```

This can be used directly with `-Xms` and `-Xmx` to determine a flexible heap size based on the current environment.

## Installation

Installation is best done using `pip` and a GitHub upstream due to PyPI's unreliability.

User install:

```
pip install --user git+https://github.com/naftulikay/heap-percent
```

System install:

```
sudo pip install git+https://github.com/naftulikay/heap-percent
```

Pin to a tag name:

```
pip install --user git+https://github.com/naftulikay/heap-percent@v0.1.0
```

## License

MIT, please see `./LICENSE`.


 [svg-travis]: https://travis-ci.org/naftulikay/heap-percent.svg?branch=develop
 [travis]: https://travis-ci.org/naftulikay/heap-percent
