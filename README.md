[![Utility Tests](https://github.com/CuckooEXE/FakeNTP/actions/workflows/utility-tests.yml/badge.svg)](https://github.com/CuckooEXE/FakeNTP/actions/workflows/utility-tests.yml)
[![CodeQL](https://github.com/CuckooEXE/FakeNTP/actions/workflows/codeql.yml/badge.svg)](https://github.com/CuckooEXE/FakeNTP/actions/workflows/codeql.yml)

# FakeNTP
A light-weight Network Time Protocol server that allows you to respond to NTP requests in a malicious manner. 

<p align="center">
  <img width="350" src="https://raw.githubusercontent.com/CuckooEXE/FakeNTP/main/FakeNTP.png">
</p>

> Inspired by [FakeDns](https://github.com/Crypt0s/FakeDns/)

## Usage
```bash
$ python3 FakeNTP.py --help
usage: FakeNTP.py [-h] [--verbose] [--ip IP] [--port PORT] [--static-time] [--time TIME] [--time-step TIME_STEP] [--passthru]
                  [--ntp-server NTP_SERVER]

FakeNTP - A light-weight fake Network Time Protocol server that allows you to trick NTP clients into changing their time.

options:
  -h, --help            show this help message and exit
  --verbose             Enable verbose output.
  --ip IP               The IP address to listen on. Default is 0.0.0.0
  --port PORT           The port to listen on. Default is 123.
  --static-time         Respond to all requests with a static time, rather than incrementing the time.
  --time TIME           The time to respond with (in epoch diff). Default is "datetime.datetime.now().timestamp()".
  --time-step TIME_STEP
                        The amount of time to increment the time by each time a request is received. If not set, then the time
                        will increment normally.
  --passthru            Pass through requests to the real NTP server.
  --ntp-server NTP_SERVER
                        The NTP server to pass requests to. Default is "pool.ntp.org".
```

This project is 100% Python3, no dependencies required (the `requirements.txt` is just for the test suites). For most use-cases, you will want to modify the response NTP structure in `FakeNTP.py:ThreadedUDPRequestHandler:handle` to best fit your needs. 


## Testing
This project contains two test suites: a simple suite to test the utility functions: `tests/test_utilities`, and more full-fledged functional tests: `test_server.py`. To run these tests, you can just execute:

```bash
$ PYTHONPATH="$PWD" python3 -m pytest --cov=FakeNTP tests/
```

## Resources
The following resources really helped me understand NTP and how to build this project:

 * [what-when-how "NTP Packet Header" Article](http://what-when-how.com/computer-network-time-synchronization/ntp-packet-header-ntp-reference-implementation-computer-network-time-synchronization/)
 * [apnic Labs](https://labs.apnic.net/?p=462)
 * [NTPv3 RFC](https://www.rfc-editor.org/rfc/rfc1305)
 * [NTPv4 RFC](https://datatracker.ietf.org/doc/html/rfc5905)