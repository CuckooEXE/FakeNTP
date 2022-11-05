"""
Test the server functionality of FakeNTP.
"""


"""
Imported Libraries

pytest - Used to run the tests.
datetime - Used to get the current time.
threading - Thread management.
socketserver - Used to create a multi-threaded server.
argparse - Mock command line arguments.
ntplib - Used to send NTP requests.
FakeNTP - Used to test the utility functions.
"""
import pytest
import datetime
import threading
import socketserver
import argparse
import ntplib
import FakeNTP


def start_server(args: argparse.Namespace) -> socketserver.ThreadingUDPServer:
    """
    Start the FakeNTP server.

    :param args: Command line arguments
    :type args: argparse.Namespace
    :return: Server
    :rtype: socketserver.ThreadingUDPServer
    """
    server = socketserver.ThreadingUDPServer(
        (args.ip, args.port), FakeNTP.ThreadedUDPRequestHandler
    )
    server.RequestHandlerClass.args = (
        args  # Store the arguments in the server object, thanks Python
    )
    threading.Thread(target=server.serve_forever).start()
    return server


def test_default_arguments():
    """
    Test the default arguments.
    """
    args = FakeNTP.build_parser().parse_args("")
    server = start_server(args)
    c = ntplib.NTPClient()
    response = c.request("127.0.0.1", version=3)
    expected = datetime.datetime.now().timestamp()
    assert abs(response.tx_time - expected) < 1
    server.shutdown()