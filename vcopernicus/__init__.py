#!/usr/bin/env python2
import sys
from shlex import split
 
import commands.coordinator
import commands.device

from .utils import commands

for k, v in commands.iteritems():
    print '%16s - %s' % (k, v.__doc__)

def run_from_command_line():
    try:
        command, line = sys.argv[1], sys.argv[2:]
        commands[command].execute(line)
    except IndexError:
        while True:
            line = split(raw_input('>>> '))
            command, line = line[0], line[1:]
            commands[command].execute(line)