#!/usr/bin/env python2

import os
import sys
from subprocess import Popen
from signal import SIGTERM

action = None
try:
    action = sys.argv[1]
except IndexError:
    print >>sys.stderr, 'Usage: %s action' % sys.argv[0]
    print >>sys.stderr, 'Availbable actions: start, stop, create_node, start_node, stop_node'

if not os.path.exists('run'):
    os.makedirs('run')

if action == 'start':
    print 'Starting coordinating webserver...'
    hypervisor_command = [
        'python',
        'lib/hypervisor/hypervisor.py'
    ]
    hypervisor = Popen(' '.join(hypervisor_command), shell=True)
    hypervisor_pidfile = os.path.join('run', 'hypervisor.pid')
    open(hypervisor_pidfile, 'w').write(str(hypervisor.pid))
elif action == 'stop':
    hypervisor_pidfile = os.path.join('run', 'hypervisor.pid')
    print 'Stopping coordinating webserver...'
    os.kill(int(open(hypervisor_pidfile, 'r').read()), SIGTERM)
    os.remove(hypervisor_pidfile)
elif action == 'create_node':
    node_name = sys.argv[2]
    print 'Creating node %s...' % node_name
    for path in ('run', 'dev', 'home'):
        os.makedirs(os.path.join(node_name, path))
elif action == 'start_node':
    node_name = sys.argv[2]
    print 'Starting node %s...' % node_name
    serial_pty = os.path.join(node_name, 'dev', 'ttyS0')
    serial_sock = os.path.join(node_name, 'run', 'ttyS0.sock')
    print '  Starting virtual serial port...'
    socat_command = [
        'socat',
        'PTY,link=%s,mode=666' % serial_pty,
        'UNIX-LISTEN:%s,fork,mode=666,unlink-early=1' % serial_sock
    ]
    socat = Popen(' '.join(socat_command), shell=True)
    socat_pidfile = os.path.join(node_name, 'run', 'socat.pid')
    open(socat_pidfile, 'w').write(str(socat.pid))
    
    print '  Starting virtual serial socket handler...'
    runner_command = [
        'python',
        'lib/device/runner.py',
        serial_sock
    ]
    runner = Popen(' '.join(runner_command), shell=True, env=os.environ.update({'IOT_NODENAME': node_name}))
    runner_pidfile = os.path.join(node_name, 'run', 'runner.pid')
    open(runner_pidfile, 'w').write(str(runner.pid))
elif action == 'stop_node':
    node_name = sys.argv[2]
    print 'Stopping node %s...' % node_name
    runner_pidfile = os.path.join(node_name, 'run', 'runner.pid')
    print '  Stopping virtual serial socket handler...'
    os.kill(int(open(runner_pidfile, 'r').read()), SIGTERM)
    os.remove(runner_pidfile)
    socat_pidfile = os.path.join(node_name, 'run', 'socat.pid')
    print '  Stopping virtual serial port...'
    os.kill(int(open(socat_pidfile, 'r').read()), SIGTERM)
    os.remove(socat_pidfile)
