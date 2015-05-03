from vcopernicus_device.transports import VCopernicusTransportBase
from vcopernicus_device.utils import register_transport


@register_transport('fd')
class VCopernicusFDTransport(VCopernicusTransportBase):
    def __init__(self, args):
        super(VCopernicusFDTransport, self).__init__(args)
        self.master = args.fd
    
    def serial_read(self):
        return ord(os.read(self.master, 1))
    
    def serial_write(self, data):
        os.write(self.master, chr(data))
    
    @staticmethod
    def parse_args(args):
        args.add_argument('-f', '--fd_number', help='set number of file description to use', required=True) 
