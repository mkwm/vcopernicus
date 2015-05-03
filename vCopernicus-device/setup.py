from setuptools import setup, find_packages

setup(
    name='vCopernicus-device',
    version='0.0.0.dev0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'vcopernicus-device = vcopernicus_device:run_entry_point',
        ],
        'vcopernicus.commands': [
            'create_node = vcopernicus_device.commands:create_node',
            'start_node = vcopernicus_device.commands:start_node',
            'stop_node = vcopernicus_device.commands:stop_node',
        ],
        'vcopernicus_device.transports': [
            'fd = vcopernicus_device.transports.fd:VCopernicusFDTransport',
            'pty = vcopernicus_device.transports.pty:VCopernicusPTYTransport',
            'unix = vcopernicus_device.transports.unix:VCopernicusUnixSocketTransport',
        ],
    },
    install_requires=[
        'eventsource',
    ],
)