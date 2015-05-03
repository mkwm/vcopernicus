#!/usr/bin/env python2
import sys
from shlex import split
import traceback
 
import commands.coordinator
import commands.device

from .utils import commands


class quit(object):
    @staticmethod
    def execute(line):
        sys.exit(0)


commands['quit'] = quit


def run_from_command_line():
    try:
        command, line = sys.argv[1], sys.argv[2:]
        commands[command].execute(line)
    except IndexError:
        while True:
            try:
                line = split(raw_input('>>> '))
            except EOFError:
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