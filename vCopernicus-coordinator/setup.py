from setuptools import setup, find_packages

setup(
    name='vCopernicus-coordinator',
    version='0.0.0.dev0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'vcopernicus-coordinator = vcopernicus_coordinator:run_entry_point',
        ],
        'vcopernicus.commands': [
            'start = vcopernicus_coordinator.commands:start',
            'stop = vcopernicus_coordinator.commands:stop',
        ],
    },
    install_requires=[
        'Flask',
        'gevent',
    ],
)