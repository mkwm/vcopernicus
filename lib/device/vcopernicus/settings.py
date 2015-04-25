import os
from socket import gethostname, socket, AF_UNIX, SOCK_STREAM

IOT_HYPERVISOR = os.environ.get('IOT_HYPERVISOR', 'localhost:8080')
IOT_NODENAME = os.environ.get('IOT_NODENAME', gethostname())
IOT_SOCKET = socket(AF_UNIX, SOCK_STREAM)
