from socket import socket, AF_UNIX, SOCK_STREAM
from vcopernicus_device.transports.fd import VCopernicusFDTransport


class VCopernicusUnixSocketTransport(VCopernicusFDTransport):
    def __init__(self, args):
        sock = socket(AF_UNIX, SOCK_STREAM)
        sock.connect(args.socket_path)
        args.fd = sock.fileno()
        super(VCopernicusUnixSocketTransport, self).__init__(args)
    
    @staticmethod
    def parse_args(args):
        args.add_argument('-p', '--socket_path', help='set path of UNIX socket to connect to', required=True) 
