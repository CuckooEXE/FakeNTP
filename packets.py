"""
Packets - Packet Definitions
"""


"""
Imported Libraries

typing - Used for type hinting.
ctypes - Used to create a C structure.
"""
from typing import Literal
import ctypes
import enum


class NTPLI(enum.IntEnum):
    """
    NTP Leap Indicator
    """
    NO_WARNING = 0
    LAST_MINUTE_61 = 1
    LAST_MINUTE_59 = 2
    ALARM = 3

class NTPVN(enum.IntEnum):
    """
    NTP Version Number
    """
    VERSION_1 = 1
    VERSION_2 = 2
    VERSION_3 = 3
    VERSION_4 = 4

class NTPMode(enum.IntEnum):
    """
    NTP Mode
    """
    RESERVED = 0
    SYMMETRIC_ACTIVE = 1
    SYMMETRIC_PASSIVE = 2
    CLIENT = 3
    SERVER = 4
    BROADCAST = 5
    NTP_CONTROL_MESSAGE = 6
    PRIVATE = 7

class NTPStratum(enum.IntEnum):
    """
    NTP Stratum
    """
    UNSPECIFIED = 0
    PRIMARY_REFERENCE = 1
    SECONDARY_REFERENCE = 2
    UNSYNCHRONIZED = 3
    RESERVED = 4


class StructHelper(object):
    def __get_value_str(self, name, fmt='{}'):
        val = getattr(self, name)
        if isinstance(val, ctypes.Array):
            val = list(val)
        return fmt.format(val)

    def __str__(self):
        result = '{}:\n'.format(self.__class__.__name__)
        maxname = max(len(f[0]) for f in self._fields_)
        for field in self._fields_:
            if len(field) == 3:
                name, type_, bitlen_ = field
            else:
                name, type_ = field
                bitlen_ = None
            value = getattr(self, name)
            result += ' {name:<{width}}: {value}\n'.format(
                    name = name,
                    width = maxname,
                    value = self.__get_value_str(name),
                    )
        return result

    def __repr__(self):
        return '{name}({fields})'.format(
                name = self.__class__.__name__,
                fields = ', '.join(
                    '{}={}'.format(name, self.__get_value_str(name, '{!r}')) for name, _ in self._fields_)
                )

    @classmethod
    def _typeof(cls, field):
        """Get the type of a field
        Example: A._typeof(A.fld)
        Inspired by stackoverflow.com/a/6061483
        """
        for name, type_ in cls._fields_:
            if getattr(cls, name) is field:
                return type_
        raise KeyError

    @classmethod
    def read_from(cls, f):
        result = cls()
        if f.readinto(result) != ctypes.sizeof(cls):
            raise EOFError
        return result

    def get_bytes(self):
        """Get raw byte string of this structure
        ctypes.Structure implements the buffer interface, so it can be used
        directly anywhere the buffer interface is implemented.
        https://stackoverflow.com/q/1825715
        """
        return bytes(self)

class NTPv3(ctypes.BigEndianStructure, StructHelper):
    _pack_ = 1
    _fields_ = [
        ('li', ctypes.c_uint8, 2),
        ('vn', ctypes.c_uint8, 3),
        ('mode', ctypes.c_uint8, 3),
        ('stratum', ctypes.c_uint8),
        ('poll', ctypes.c_uint8),
        ('precision', ctypes.c_uint8),
        ('root_delay', ctypes.c_uint32),
        ('root_dispersion', ctypes.c_uint32),
        ('reference_identifier', ctypes.c_uint32),
        ('reference_timestamp', ctypes.c_uint64),
        ('originate_timestamp', ctypes.c_uint64),
        ('receive_timestamp', ctypes.c_uint64),
        ('transmit_timestamp', ctypes.c_uint64)
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.li = 0
        self.vn = 3
        self.mode = 4
        self.stratum = 0
        self.poll = 0
        self.precision = 0
        self.root_delay = 0
        self.root_dispersion = 0
        self.reference_identifier = 0
        self.reference_timestamp = 0
        self.originate_timestamp = 0
        self.receive_timestamp = 0
        self.transmit_timestamp = 0
    