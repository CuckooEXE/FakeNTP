"""
FakeNTP - A light-weight fake Network Time Protocol server that allows you to trick NTP clients into changing their time.
"""


"""
Imported Libraries

argparse - Used to parse command line arguments.
datetime - Used to get the current time.
socketserver - Used to create a multi-threaded server.
logging - Used to generate log messages.
signal - Used to capture SIGINT for graceful shutdown.
sys - Used to exit the process.
"""
import argparse
import datetime
import socketserver
import logging
import signal
import sys


"""
Global Variables

"""


def signal_handler(signal: int, frame: None) -> None:
    """Handle the SIGINT signal

    :param signal: Signal that was received
    :type signal: int
    :param frame: Signal's frame
    :type frame: None
    """
    if signal != signal.SIGINT:
        logging.error("Received unexpected signal: {}".format(signal))
        return
    logging.info("Shutting down FakenTP server...")
    sys.exit(0)


class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data, sock = self.request
        logging.debug("Received request from: {}:{}".format(*self.client_address))
        sock.sendto(b'RESPONSE: ' + data, self.client_address)


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(description='FakeNTP - A light-weight fake Network Time Protocol server that allows you to trick NTP clients into changing their time.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output.')
    parser.add_argument('-i', '--ip', type=str, default='0.0.0.0', help='The IP address to listen on. Default is 0.0.0.0')
    parser.add_argument('-p', '--port', type=int, default=123, help='The port to listen on. Default is 123.')
    parser.add_argument('--static-time', action='store_true', help='Respond to all requests with a static time, rather than incrementing the time.')
    parser.add_argument('--time', type=float, default=datetime.datetime.utcnow().timestamp(), help='The time to respond with (in epoch diff). Default is "datetime.datetime.utcnow().timestamp()".')
    args = parser.parse_args()

    # Create logger
    logging.basicConfig(format="[%(asctime)s][%(levelname)s][%(funcName)s]: %(message)s", level=(logging.DEBUG if args.verbose else logging.INFO))

    # Create the SIGINT signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Create the server
    logging.debug("Creating server on {}:{}".format(args.ip, args.port))
    server = socketserver.ThreadingUDPServer((args.ip, args.port), ThreadedUDPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()