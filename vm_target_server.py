#!/usr/bin/env python2

from SimpleXMLRPCServer import SimpleXMLRPCServer
from argparse import ArgumentParser
from sys import argv
import i3ipc
import xmlrpclib


def safe_parse(v, t, d):
    _ret = d
    try:
        _ret = t(v)
    except ValueError:
        _ret = d
    return _ret


class VmTargetServer(object):
    def __init__(self):
        self._index = 0
        self._targets = [ None, "foo", "bar", "baz" ]
        self._funcs = {}

        # Register Function
        self._register("get_name", self.get_name)
        self._register("move", self.move)
        self._register("run", self.run)
        self._register("run_on", self.run_on)
        self._register("system.listMethods", self._list_methods)

    def _register(self, name, func):
        self._funcs[name] = {
            "fn": func,
            "doc": func.__doc__ or ""
        }

    def _dispatch(self, name, *args):
        _t = self._funcs.get(name)
        if not _t:
            raise Exception

        _args = args[0]
        _ret = _t["fn"](*_args)
        return _ret

    def _list_methods(self, x=None):
        """ List the supported methods """
        if x:
            _key = x[0]
            _obj = self._funcs.get(_key)
            return " - ".join([_key, _obj["doc"]])
        return "\n".join([" - ".join([x, self._funcs[x]["doc"]]) for x in self._funcs.keys()])

    def _normalize_index(self, i):
        return i % len(self._targets)

    def get_name(self):
        """ Get the name of current target """
        return self._targets[self._index] or "LOCAL"

    def move(self, count):
        """ Move to another target by 'n' """
        _index = self._index + safe_parse(count, int, 0)
        self._index = self._normalize_index(_index)
        return count

    def run(self, command):
        """ Execute a command on the current target """
        _target = self._targets[self._index]
        return self.run_on(_target, command)

    def run_on(self, target, command):
        """ Execute a command on a specific target """
        conn = i3ipc.Connection()
        if target:
            _command = "exec ssh {} '{}'".format(target, command)
        else:
            _command = "exec '{}'".format(command)
        conn.command(_command)
        return _command


def get_opts():
    ap = ArgumentParser(description="Run Target VM Manager")
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
    return ap.parse_args(argv[1:])


if __name__ == "__main__":
    opts = get_opts()
    server = SimpleXMLRPCServer((opts.host, opts.port), allow_none=True)
    server.register_instance(VmTargetServer())
    print("Listening on {}:{}".format(opts.host, opts.port))
    server.serve_forever()
