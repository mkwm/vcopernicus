from vcopernicus_device.transports.fd import VCopernicusFDTransport
from vcopernicus_device.utils import register_transport


@register_transport('pty')
class VCopernicusPTYTransport(VCopernicusFDTransport):
    def __init__(self, args):
        args.fd, slave = os.openpty()
        os.unlink(args.pty_path)
        os.symlink(os.ttyname(slave), args.pty_path)
        super(VCopernicusPTYTransport, self).__init__(args)
    
    @staticmethod
    def parse_args(args):
        args.add_argument('-p', '--pty_path', help='set path of virtual serial port to create', required=True) 
