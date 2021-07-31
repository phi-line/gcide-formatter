from setuptools import setup

setup(
    name='gcide',
    version='1.0.0-dev01',
    py_modules=['gcide'],
    install_requires=[
        'Click', 'bs4', 'lxml', 'requests'
    ],
    entry_points={
        'console_scripts': [
            'gcide = gcide:cli',
        ],
    },
)
