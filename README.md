[![Utility Tests](https://github.com/CuckooEXE/FakeNTP/actions/workflows/utility-tests.yml/badge.svg)](https://github.com/CuckooEXE/FakeNTP/actions/workflows/utility-tests.yml)

# FakeNTP
A light-weight fake Network Time Protocol server that allows you to trick NTP clients into changing their time.

> Inspired by [FakeDns](https://github.com/Crypt0s/FakeDns/)

![FakeNTP](FakeNTP.png)

## Usage
To use FakeNTP, you can ues the Docker container, or just run the Python script itself:
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

## Testing
This project has two test suites: a `pytest` suite in `tests/` that tests the utility functions, and a set of Github Actions that test the functionality of the project.

To run these tests, you can look at the tests in `.github/workflows/{utility,functional}-tests.yml`.
