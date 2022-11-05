"""
Test the server functionality of FakeNTP.
"""


"""
Imported Libraries

pytest - Used to run the tests.
datetime - Used to get the current time.
threading - Thread management.
socketserver - Used to create a multi-threaded server.
ntplib - Used to send NTP requests.
FakeNTP - Used to test the utility functions.
"""
import pytest
import datetime
import threading
import socketserver
import ntplib
import FakeNTP


@pytest.fixture
def server(request: pytest.FixtureRequest):
    """Setup and teardown server

    :param request: Pytest Request
    :type request: pytest.FixtureRequest
    :yield: Server object
    :rtype: Iterator[FakeNTP.ThreadedUDPRequestHandler]
    """
    args = FakeNTP.build_parser().parse_args(
        request.param.split(" ") if request.param else []
    )
    server = socketserver.ThreadingUDPServer(
        (args.ip, args.port), FakeNTP.ThreadedUDPRequestHandler
    )
    server.RequestHandlerClass.args = args
    threading.Thread(target=server.serve_forever).start()
    yield server
    server.shutdown()


@pytest.mark.parametrize("server", [""], indirect=True)
def test_default_arguments(server):
    """
    Test the default arguments.
    """
    c = ntplib.NTPClient()
    response = c.request("127.0.0.1", version=3)
    expected = datetime.datetime.now().timestamp()
    assert abs(response.tx_time - expected) < 1


@pytest.mark.parametrize("server", ["--port 8080"], indirect=True)
def test_port(server):
    """
    Test the --port argument.
    """
    c = ntplib.NTPClient()
    with pytest.raises(ntplib.NTPException):
        response = c.request("127.0.0.1", version=3)
    response = c.request("127.0.0.1", port=8080, version=3)
    expected = datetime.datetime.now().timestamp()
    assert abs(response.tx_time - expected) < 1
