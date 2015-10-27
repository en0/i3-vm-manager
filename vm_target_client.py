#!/usr/bin/env python2

import xmlrpclib
from argparse import ArgumentParser
from sys import argv



def get_opts():
    ap = ArgumentParser()
    ap.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="The IP of the address to bind."
    )
    ap.add_argument(
        "--port",
        type=int,
        default="8189",
        help="The Port to bind."
    )
    ap.add_argument(
        '-n', '--next',
        action="store_true"
    )
    ap.add_argument(
        '-p', '--prev',
        action="store_true"
    )
    ap.add_argument(
        '-r', '--run',
        type=str
    )
    ap.add_argument(
        '-g', '--get',
        action="store_true"
    )
    return ap.parse_args(argv[1:])


if __name__ == "__main__":
    opts = get_opts()

    proxy = xmlrpclib.ServerProxy("http://{}:{}/".format(opts.host, opts.port))

    _ran_something = False
    if opts.next:
        print proxy.move(1)
        _ran_something = True
    if opts.prev:
        print proxy.move(-1)
        _ran_something = True
    if opts.run:
        print proxy.run(opts.run)
        _ran_something = True
    if opts.get:
        print proxy.get_name()
        _ran_something = True

    if not _ran_something:
        print proxy.system.listMethods()
