# FakeNTP
A light-weight fake Network Time Protocol server that allows you to trick NTP clients into changing their time.

> Inspired by [FakeDns](https://github.com/Crypt0s/FakeDns/)

## Usage
To use FakeNTP, you can ues the Docker container, or just run the Python script itself:
```bash
$ python3 FakeNTP.py --help
usage: FakeNTP.py [-h] [-v] [-i IP] [-p PORT] [--static-time] [--time TIME]

FakeNTP - A light-weight fake Network Time Protocol server that allows you to trick NTP clients into
changing their time.

options:
  -h, --help            show this help message and exit
  -v, --verbose         Enable verbose output.
  -i IP, --ip IP        The IP address to listen on. Default is 0.0.0.0
  -p PORT, --port PORT  The port to listen on. Default is 123.
  --static-time         Respond to all requests with a static time, rather than incrementing the time.
  --time TIME           The time to respond with (in epoch diff). Default is
                        "datetime.datetime.now().timestamp()".
```
