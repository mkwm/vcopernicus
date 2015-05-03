import os
import sys
from subprocess import Popen
from signal import SIGTERM

from vcopernicus.utils import register


@register()
class create_node(object):
    '''Create virtual device directory structure'''
    @staticmethod
    def execute(argv):
        node_name = argv[0]
        print 'Creating node %s...' % node_name
        for path in ('run', 'dev', 'home'):
            os.makedirs(os.path.join(node_name, path))
        open(os.path.join(node_name, 'home', 'code.py'), 'w').write(BOOTSTRAP_TEMPLATE)


@register()
class start_node(object):
    '''Start virtual device'''
    @staticmethod
    def execute(argv):
        node_name = argv[0]
        print 'Starting node %s...' % node_name
        serial_pty = os.path.join(node_name, 'dev', 'ttyS0')
        serial_sock = os.path.join(node_name, 'run', 'ttyS0.sock')
        print '  Starting virtual serial port...'
        socat_command = [
            'socat',
            'PTY,link=%s,mode=666' % serial_pty,
            'UNIX-LISTEN:%s,fork,mode=666,unlink-early=1' % serial_sock
        ]
        #socat = Popen(' '.join(socat_command), shell=True)
        #socat_pidfile = os.path.join(node_name, 'run', 'socat.pid')
        #open(socat_pidfile, 'w').write(str(socat.pid))
        
        print '  Starting virtual serial socket handler...'
        runner = Popen('vcopernicus-device %s' % serial_pty, shell=True, env=os.environ.update({'IOT_NODENAME': node_name}))
        runner_pidfile = os.path.join(node_name, 'run', 'runner.pid')
        open(runner_pidfile, 'w').write(str(runner.pid))


@register()
class stop_node(object):
    '''Stop virtual device'''
    @staticmethod
    def execute(argv):
        node_name = argv[0]
        print 'Stopping node %s...' % node_name
        runner_pidfile = os.path.join(node_name, 'run', 'runner.pid')
        print '  Stopping virtual serial socket handler...'
        os.kill(int(open(runner_pidfile, 'r').read()), SIGTERM)
        os.remove(runner_pidfile)
        socat_pidfile = os.path.join(node_name, 'run', 'socat.pid')
        #print '  Stopping virtual serial port...'
        #os.kill(int(open(socat_pidfile, 'r').read()), SIGTERM)
        #os.remove(socat_pidfile) 