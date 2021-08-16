from setuptools import setup

setup(
    name='gcide',
    version='1.0.0',
    py_modules=[
        'gcide',
        'definitions_json',
        'definitions_sqlite',
        'gcide_downloader',
        'core'
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
