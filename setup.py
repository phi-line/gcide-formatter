from setuptools import setup

setup(
    name='gcide',
    version='1.0.0-dev01',
    py_modules=[
        'gcide',
        'definitions_json',
        'definitions_sqlite',
        'gcide_downloader',
        'gcide_parser'
    ],
    install_requires=[
        'Click', 'bs4', 'lxml', 'requests'
    ],
    entry_points={
        'console_scripts': [
            'gcide = gcide:cli',
        ],
    },
)
