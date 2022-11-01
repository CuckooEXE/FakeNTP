"""
FakeNTP - A light-weight fake Network Time Protocol server that allows you to trick NTP clients into changing their time.
"""


"""
Imported Libraries

argparse - Used to parse command line arguments.
"""
import argparse


"""
Global Variables

"""


def main():
    parser = argparse.ArgumentParser(description='FakeNTP - A light-weight fake Network Time Protocol server that allows you to trick NTP clients into changing their time.')
    parser.add_argument('-i', '--ip', type=str, default='0.0.0.0', help='The IP address to listen on. Default is 0.0.0.0')
    parser.add_argument('-p', '--port', type=int, default=123, help='The port to listen on. Default is 123.')
    parser.add_argument('--static-time', action='store_true', help='Respond to all requests with a static time, rather than incrementing the time.')
    parser.add_argument('time', type=str, default='01/01/1970 00:00:00', help='The time to respond with. Default is 01/01/1970 00:00:00.')
    args = parser.parse_args()
    

if __name__ == '__main__':
    main()