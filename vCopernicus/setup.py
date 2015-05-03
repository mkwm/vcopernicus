from setuptools import setup, find_packages

setup(
    name='vCopernicus',
    version='0.0.0.dev0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'vcopernicus = vcopernicus:run_entry_point',
        ],
    },
    include_package_data=True,
)