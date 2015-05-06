# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='vCopernicus',
    version='0.0.0.dev0',
    url='https://github.com/mkwm/iot-vcopernicus',
    author='Mateusz Małek',
    author_email='mamalek@student.agh.edu.pl',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'vcopernicus = vcopernicus:run_entry_point',
        ],
    },
    include_package_data=True,
)