"""Tests for filesize humanizing."""

from __future__ import annotations

import pytest

import humanize


@pytest.mark.parametrize(
    "test_args, expected",
    [
        ([300], "300 Bytes"),
        (["1000"], "1.0 kB"),
        ([10**3], "1.0 kB"),
        ([10**6], "1.0 MB"),
        ([10**9], "1.0 GB"),
        ([10**12], "1.0 TB"),
        ([10**15], "1.0 PB"),
        ([10**18], "1.0 EB"),
        ([10**21], "1.0 ZB"),
        ([10**24], "1.0 YB"),
        ([10**27], "1.0 RB"),
        ([10**30], "1.0 QB"),
        ([1000**1 * 31], "31.0 kB"),
        ([1000**2 * 32], "32.0 MB"),
        ([1000**3 * 33], "33.0 GB"),
        ([1000**4 * 34], "34.0 TB"),
        ([1000**5 * 35], "35.0 PB"),
        ([1000**6 * 36], "36.0 EB"),
        ([1000**7 * 37], "37.0 ZB"),
        ([1000**8 * 38], "38.0 YB"),
        ([1000**9 * 39], "39.0 RB"),
        ([1000**10 * 40], "40.0 QB"),
        ([300, True], "300 Bytes"),
        ([1024**1 * 31, True], "31.0 KiB"),
        ([1024**2 * 32, True], "32.0 MiB"),
        ([1024**3 * 33, True], "33.0 GiB"),
        ([1024**4 * 34, True], "34.0 TiB"),
        ([1024**5 * 35, True], "35.0 PiB"),
        ([1024**6 * 36, True], "36.0 EiB"),
        ([1024**7 * 37, True], "37.0 ZiB"),
        ([1024**8 * 38, True], "38.0 YiB"),
        ([1024**9 * 39, True], "39.0 RiB"),
        ([1024**10 * 40, True], "40.0 QiB"),
        ([1000**1 * 31, True], "30.3 KiB"),
        ([1000**2 * 32, True], "30.5 MiB"),
        ([1000**3 * 33, True], "30.7 GiB"),
        ([1000**4 * 34, True], "30.9 TiB"),
        ([1000**5 * 35, True], "31.1 PiB"),
        ([1000**6 * 36, True], "31.2 EiB"),
        ([1000**7 * 37, True], "31.3 ZiB"),
        ([1000**8 * 38, True], "31.4 YiB"),
        ([1000**9 * 39, True], "31.5 RiB"),
        ([1000**10 * 40, True], "31.6 QiB"),
        ([1000**1 * 31, False, True], "30.3K"),
        ([1000**2 * 32, False, True], "30.5M"),
        ([1000**3 * 33, False, True], "30.7G"),
        ([1000**4 * 34, False, True], "30.9T"),
        ([1000**5 * 35, False, True], "31.1P"),
        ([1000**6 * 36, False, True], "31.2E"),
        ([1000**7 * 37, False, True], "31.3Z"),
        ([1000**8 * 38, False, True], "31.4Y"),
        ([1000**9 * 39, False, True], "31.5R"),
        ([1000**10 * 40, False, True], "31.6Q"),
        ([300, False, True], "300B"),
        ([3000, False, True], "2.9K"),
        ([3000000, False, True], "2.9M"),
        ([1024, False, True], "1.0K"),
        ([1, False, False], "1 Byte"),
        ([1.0, False, False], "1 Byte"),
        (["1", False, False], "1 Byte"),
        ([3141592, False, False, "%.2f"], "3.14 MB"),
        ([3000, False, True, "%.3f"], "2.930K"),
        ([3000000000, False, True, "%.0f"], "3G"),
        ([10**26 * 30, True, False, "%.3f"], "2.423 RiB"),
        ([1.123456789], "1 Bytes"),
        ([1.123456789 * 10**3], "1.1 kB"),
        ([1.123456789 * 10**6], "1.1 MB"),
        ([1.123456789, False, True], "1B"),
        ([1.123456789 * 10**3, False, True], "1.1K"),
        ([1.123456789 * 10**6, False, True], "1.1M"),
        # Rounding must not leave the mantissa at the base while a larger suffix
        # is available: 999999 is 999.999 kB, which the "%.1f" format rounds to
        # 1000.0 and must carry into 1.0 MB rather than render as "1000.0 kB".
        ([999999], "1.0 MB"),
        ([999999999], "1.0 GB"),
        ([999999999999], "1.0 TB"),
        ([1024**2 - 1, True], "1.0 MiB"),
        ([1024**3 - 1, True], "1.0 GiB"),
        ([1024**2 - 1, False, True], "1.0M"),
    ],
)
def test_naturalsize(test_args: list[int] | list[int | bool], expected: str) -> None:
    assert humanize.naturalsize(*test_args) == expected

    # Retest with negative input
    if isinstance(test_args[0], int):
        test_args[0] *= -1
    else:
        test_args[0] = f"-{test_args[0]}"

    assert humanize.naturalsize(*test_args) == "-" + expected


@pytest.mark.parametrize(
    "binary, gnu, expected",
    [
        (False, False, ["2 kB", "1.5 kB", "1.54 kB", "1.536 kB", "1.536000 kB"]),
        (True, False, ["2 KiB", "1.5 KiB", "1.50 KiB", "1.500 KiB", "1.500000 KiB"]),
        (False, True, ["2K", "1.5K", "1.50K", "1.500K", "1.500000K"]),
        (True, True, ["2K", "1.5K", "1.50K", "1.500K", "1.500000K"]),
    ],
)
@pytest.mark.parametrize("precision, index", [(0, 0), (1, 1), (2, 2), (3, 3), (6, 4)])
def test_precision_matrix(binary, gnu, expected, precision, index):
    assert humanize.naturalsize(1536, binary, gnu, precision=precision) == expected[index]
    assert humanize.naturalsize(-1536, binary, gnu, precision=precision) == "-" + expected[index]


@pytest.mark.parametrize("fmt", ["%.0f", "invalid"])
def test_precision_overrides_format(fmt):
    assert humanize.naturalsize(3000, format=fmt, precision=2) == "3.00 kB"


def test_precision_none_and_positional_compatibility():
    assert humanize.naturalsize(3000, False, True, "%.3f", precision=None) == "2.930K"
    with pytest.raises(TypeError):
        humanize.naturalsize(3000, False, True, "%.3f", 2)


@pytest.mark.parametrize("binary, gnu, below_base", [(False, False, 999), (True, False, 1023), (False, True, 1023)])
@pytest.mark.parametrize("value, expected, gnu_expected", [
    (0, "0 Bytes", "0B"), (0.5, "0 Bytes", "0B"), (-0.5, "0 Bytes", "0B"),
    (1, "1 Byte", "1B"), (-1, "-1 Byte", "-1B"),
    (300, "300 Bytes", "300B"), (-300, "-300 Bytes", "-300B"),
    ("below_base", None, None),
])
def test_precision_bytes_compatibility(binary, gnu, below_base, value, expected, gnu_expected):
    if value == "below_base":
        value = below_base
        expected = "999 Bytes" if below_base == 999 else "1023 Bytes"
        gnu_expected = "1023B"
    assert humanize.naturalsize(value, binary, gnu, precision=2) == (gnu_expected if gnu else expected)


@pytest.mark.parametrize("binary, gnu, value, expected", [
    (False, False, 1000, "1.00 kB"), (True, False, 1024, "1.00 KiB"),
    (False, True, 1024, "1.00K"), (False, False, 999999, "1.00 MB"),
    (True, False, 1024**2 - 1, "1.00 MiB"), (False, True, 1024**2 - 1, "1.00M"),
    (False, False, 10**34 * 3, "30000.00 QB"),
    (True, False, 1024**10 * 3, "3.00 QiB"), (False, True, 1024**10 * 3, "3.00Q"),
])
def test_precision_symmetric_boundaries(binary, gnu, value, expected):
    assert humanize.naturalsize(value, binary, gnu, precision=2) == expected
    assert humanize.naturalsize(-value, binary, gnu, precision=2) == "-" + expected


@pytest.mark.parametrize("binary, gnu, value, expected", [
    (False, False, 999999, "999.999 kB"),
    (True, False, 1024**2 - 1, "1023.999 KiB"),
    (False, True, 1024**2 - 1, "1023.999K"),
])
def test_precision_carry_boundary(binary, gnu, value, expected):
    assert humanize.naturalsize(value, binary, gnu, precision=3) == expected
    assert humanize.naturalsize(-value, binary, gnu, precision=3) == "-" + expected


@pytest.mark.parametrize("binary, gnu, value, expected", [
    (False, False, 3000, "3.0 kB"), (True, False, 3000.0, "2.9 KiB"),
    (False, True, "3000", "2.9K"), (False, False, 1, "1 Byte"),
])
def test_existing_negative_symmetry(binary, gnu, value, expected):
    assert humanize.naturalsize(value, binary, gnu) == expected
    assert humanize.naturalsize(f"-{value}", binary, gnu) == "-" + expected


@pytest.mark.parametrize("binary, gnu, expected", [(False, False, "3.000 kB"), (True, False, "2.930 KiB"), (False, True, "2.930K")])
def test_custom_format_symmetry(binary, gnu, expected):
    assert humanize.naturalsize(3000, binary, gnu, "%.3f") == expected
    assert humanize.naturalsize(-3000, binary, gnu, "%.3f") == "-" + expected


@pytest.mark.parametrize("binary, gnu", [(False, False), (True, False), (False, True)])
@pytest.mark.parametrize("value", [1, 3000])
@pytest.mark.parametrize("precision, error", [(-1, ValueError), (-3, ValueError), (True, TypeError), (False, TypeError), (2.0, TypeError), (-1.0, TypeError), (float('nan'), TypeError), (float('inf'), TypeError), ("2", TypeError)])
def test_invalid_precision(binary, gnu, value, precision, error):
    with pytest.raises(error):
        humanize.naturalsize(value, binary, gnu, precision=precision)


def test_existing_out_of_scope_formats():
    assert humanize.naturalsize(0.5) == humanize.naturalsize(-0.5) == "0 Bytes"
    assert humanize.naturalsize(0.5, gnu=True) == humanize.naturalsize(-0.5, gnu=True) == "0B"
    assert humanize.naturalsize(3000, gnu=True, format="%+.1f") == "+2.9K"
    assert humanize.naturalsize(-3000, gnu=True, format="%+.1f") == "-2.9K"


def test_precision_accepts_int_subclass():
    class Precision(int):
        pass

    assert humanize.naturalsize(3000, precision=Precision(2)) == "3.00 kB"
