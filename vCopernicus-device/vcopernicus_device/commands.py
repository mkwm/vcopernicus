import os
from shutil import copytree
import sys
from subprocess import Popen
from signal import SIGTERM


class create_node(object):
    '''Create virtual device directory structure'''
    @staticmethod
    def execute(argv):
        node_name = argv[0]
        BASE_DIR = os.path.dirname(os.path.realpath(__file__))
        TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates', 'node')
        print 'Creating node %s...' % node_name
        copytree(TEMPLATE_DIR, node_name)


class start_node(object):
    '''Start virtual device'''
    @staticmethod
    def execute(argv):
        node_name = argv[0]
        print 'Starting node %s...' % node_name
        serial_pty = os.path.join(node_name, 'dev', 'ttyS0')
        print '  Starting virtual serial socket handler...'
        runner = Popen('vcopernicus-device pty -p %s' % serial_pty, shell=True, env=os.environ.update({'IOT_NODENAME': node_name}))
        runner_pidfile = os.path.join(node_name, 'run', 'runner.pid')
        open(runner_pidfile, 'w').write(str(runner.pid))


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