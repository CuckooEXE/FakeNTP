"""
Test the utility functions of FakeNTP.
"""


"""
Imported Libraries

pytest - Used to run the tests.
datetime - Used to get the current time.
FakeNTP - Used to test the utility functions.
"""
import pytest
import datetime
import FakeNTP


def test_system_to_ntp_time():
    """
    Test the system_to_ntp_time function.
    """
    timestamp = 0
    assert FakeNTP.system_to_ntp_time(timestamp) == FakeNTP._NTP_DELTA
    timestamp = 2**32
    with pytest.raises(ValueError):
        FakeNTP.system_to_ntp_time(timestamp)


def test_to_int():
    """
    Test the _to_int function.
    """
    timestamp = 0
    assert FakeNTP._to_int(timestamp) == 0
    timestamp = 1.5
    assert FakeNTP._to_int(timestamp) == 1


def test_to_frac():
    """
    Test the _to_frac function.
    """
    timestamp = 0
    assert FakeNTP._to_frac(timestamp) == 0
    timestamp = 1.5
    assert FakeNTP._to_frac(timestamp) == 2147483648


def test_system_epoch():
    """
    Test the system_epoch function.
    """
    assert FakeNTP._SYSTEM_EPOCH == datetime.date(1970, 1, 1)


def test_ntp_epoch():
    """
    Test the ntp_epoch function.
    """
    assert FakeNTP._NTP_EPOCH == datetime.date(1900, 1, 1)
