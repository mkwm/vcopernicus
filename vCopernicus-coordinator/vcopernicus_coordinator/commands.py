import os
import sys
from subprocess import Popen
from signal import SIGTERM


class start(object):
    '''Start coordinating webserver'''
    @staticmethod
    def execute(argv):
        print 'Starting coordinating webserver...'
        hypervisor = Popen('vcopernicus-coordinator', shell=True)
        hypervisor_pidfile = os.path.join('run', 'hypervisor.pid')
        open(hypervisor_pidfile, 'w').write(str(hypervisor.pid))


class stop(object):
    '''Stop coordinating webserver'''
    @staticmethod
    def execute(argv):
        hypervisor_pidfile = os.path.join('run', 'hypervisor.pid')
        print 'Stopping coordinating webserver...'
        os.kill(int(open(hypervisor_pidfile, 'r').read()), SIGTERM)
        os.remove(hypervisor_pidfile)