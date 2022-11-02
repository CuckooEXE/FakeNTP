"""
FakeNTP - A light-weight fake Network Time Protocol server that allows you to
            trick NTP clients into changing their time.
"""


"""
Imported Libraries

argparse - Used to parse command line arguments.
datetime - Used to get the current time.
socketserver - Used to create a multi-threaded server.
logging - Used to generate log messages.
signal - Used to capture SIGINT for graceful shutdown.
sys - Used to exit the process.
time - Used to get the epoch time.
packets - Used to create the NTP packet.
"""
import argparse
import datetime
import socketserver
import logging
import signal
import sys
import time
from packets import NTPLI, NTPVN, NTPMode, NTPStratum, NTPv3


"""
Global Variables
(Taken from https://github.com/cf-natali/ntplib/blob/08d0f7ef766715a52f472901de5e382c8f773855/ntplib.py#L49)
_SYSTEM_EPOCH - System Epoch Time
_NTPEPOCH - NTP Epoch Time
_NTP_DELTA - Difference between the NTP and System Epochs
"""
_SYSTEM_EPOCH = datetime.date(*time.gmtime(0)[0:3])
_NTP_EPOCH = datetime.date(1900, 1, 1)
_NTP_DELTA = (_SYSTEM_EPOCH - _NTP_EPOCH).days * 24 * 3600


def signal_handler(sig: int, frame: None) -> None:
    """Handle the SIGINT signal
    :param sig: Signal that was received
    :type sig: int
    :param frame: Signal's frame
    :type frame: None
    """
    if sig != signal.SIGINT:
        logging.error("Received unexpected signal: {}".format(sig))
        return
    logging.info("Shutting down FakenTP server...")
    sys.exit(0)


def system_to_ntp_time(timestamp: float) -> float:
    """
    Convert system time format to ntp time format
    (Taken from https://github.com/cf-natali/ntplib/blob/08d0f7ef766715a52f472901de5e382c8f773855/ntplib.py#L49)

    :param timestamp: Timestamp
    :type timestamp: float
    :return: Timestamp in ntp format
    :rtype: float
    """
    ntp_time = timestamp + _NTP_DELTA
    if ntp_time >= 2**32:
        raise ValueError(
            "Timestamp {} is beyond NTPv3 rollover".format(timestamp)
        )
    return ntp_time


def _to_int(timestamp: int):
    """Get the integral part of a timestamp
    (Taken from https://github.com/cf-natali/ntplib/blob/08d0f7ef766715a52f472901de5e382c8f773855/ntplib.py#L49)

    :param timestamp: timestamp
    :type timestamp: int
    :return: Integral part
    :rtype: int
    """
    return int(timestamp)


def _to_frac(timestamp: int, bits: int = 32):
    """Get the fractional part of a timestamp
    (Taken from https://github.com/cf-natali/ntplib/blob/08d0f7ef766715a52f472901de5e382c8f773855/ntplib.py#L49)

    :param timestamp: Timestamp
    :type timestamp: int
    :param bits: Number of bits of the fractional part
    :type bits: int
    :return: Fractional part
    :rtype: int
    """
    return int(abs(timestamp - _to_int(timestamp)) * 2**bits)


class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data, sock = self.request
        logging.debug(
            "Received {} bytes from: {}:{}".format(
                len(data), *self.client_address
            )
        )

        # Update the time if we're using a static time
        if not self.args.static_time:
            self.args.time = datetime.datetime.now().timestamp()
        now = system_to_ntp_time(self.args.time)

        # Parse the NTP request
        request = NTPv3.from_buffer_copy(data)

        # Build the NTP response
        response = NTPv3()
        response.li = NTPLI.NO_WARNING
        response.vn = NTPVN.VERSION_4
        response.mode = NTPMode.SERVER
        response.stratum = NTPStratum.SECONDARY_REFERENCE
        response.poll = 1
        response.precision = 0xFFFFFFE7
        response.root_delay = _to_int(32) << 16 | _to_frac(32, 16)
        response.root_dispersion = _to_int(0.000030) << 16 | _to_frac(
            0.000030, 16
        )
        response.reference_identifier = int.from_bytes(
            b"NIST", byteorder="big"
        )  # NIST Public Modem
        response.reference_timestamp = _to_int(now - 30) << 32 | _to_frac(
            now - 30, 32
        )  # 30 seconds ago, just a lie to make it believable :)
        response.originate_timestamp = request.transmit_timestamp
        response.receive_timestamp = _to_int(now) << 32 | _to_frac(now, 32)
        response.transmit_timestamp = _to_int(now) << 32 | _to_frac(now, 32)

        logging.debug(
            "Responding with time: {}".format(
                datetime.datetime.fromtimestamp(now - _NTP_DELTA)
            )
        )
        logging.debug("Request:\n{}".format(request))
        logging.debug("Response:\n{}".format(response))
        sock.sendto(response.get_bytes(), self.client_address)

        # If we have a timestep, then we need to increment the time by that much
        if self.args.time_step:
            self.args.time += datetime.timedelta(seconds=self.args.time_step)


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(
        description="FakeNTP - A light-weight fake Network Time Protocol server that allows you to trick NTP clients into changing their time."
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output."
    )
    parser.add_argument(
        "--ip",
        type=str,
        default="0.0.0.0",
        help="The IP address to listen on. Default is 0.0.0.0",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=123,
        help="The port to listen on. Default is 123.",
    )
    parser.add_argument(
        "--static-time",
        action="store_true",
        help="Respond to all requests with a static time, rather than incrementing the time.",
    )
    parser.add_argument(
        "--time",
        type=float,
        default=datetime.datetime.now().timestamp(),
        help='The time to respond with (in epoch diff). Default is "datetime.datetime.now().timestamp()".',
    )
    parser.add_argument(
        "--time-step",
        type=int,
        default=0,
        help="The amount of time to increment the time by each time a request is received. If not set, then the time will increment normally.",
    )
    parser.add_argument(
        "--passthru",
        default=False,
        action="store_true",
        help="Pass through requests to the real NTP server.",
    )
    parser.add_argument(
        "--ntp-server",
        type=str,
        default="pool.ntp.org",
        help='The NTP server to pass requests to. Default is "pool.ntp.org".',
    )
    args = parser.parse_args()

    # Validate the arguments
    if args.time_step and args.static_time:
        raise ValueError("Cannot use --time-step and --static-time together.")

    # Create logger
    logging.basicConfig(
        format="[%(levelname)s][%(asctime)s][%(funcName)s]: %(message)s",
        level=(logging.DEBUG if args.verbose else logging.INFO),
    )

    # Create the SIGINT signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Create the server
    logging.debug("Creating server on {}:{}".format(args.ip, args.port))
    server = socketserver.ThreadingUDPServer(
        (args.ip, args.port), ThreadedUDPRequestHandler
    )
    server.RequestHandlerClass.args = (
        args  # Store the arguments in the server object, thanks Python
    )
    server.serve_forever()


if __name__ == "__main__":
    main()
