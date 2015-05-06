#!/usr/bin/env python2
from collections import OrderedDict
import sys
from shlex import split
import traceback

from pkg_resources import iter_entry_points


main_loop = True


commands = OrderedDict()
for entry_point in iter_entry_points('vcopernicus.commands'):
    try:
        commands[entry_point.name] = entry_point.load()
    except Exception:
        print 'Failed to load', entry_point.name


class quit(object):
    '''Exit commands shell'''
    @staticmethod
    def execute(line):
        global main_loop
        main_loop = False


class help(object):
    '''Show available commands list'''
    @staticmethod
    def execute(line):
        global commands
        for name, command in commands.iteritems():
            if command.__doc__:
                print '%16s - %s' % (name, command.__doc__)


commands['help'] = help


def run_entry_point():
    try:
        command, line = sys.argv[1], sys.argv[2:]
        commands[command].execute(line)
    except IndexError:
        commands['quit'] = quit
        print "Welcome to vCopernicus management shell"
        print "To see list of available commands, type 'help'"
        while main_loop:
            try:
                line = split(raw_input('>>> '))
            except (KeyboardInterrupt, EOFError):
                print ''
                break
            func = None
            try:
                command, line = line[0], line[1:]
                func = commands[command].execute
            except IndexError:
                continue
            except KeyError:
                print 'No such command'
                continue
            try:
                func(line)
            except Exception as e:
                print traceback.format_exc()