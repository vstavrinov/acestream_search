from setuptools import setup

setup(
    name='acestream_search',
    version='1.0.2',
    packages=['acestream_search'],
    package_dir={'acestream_search': '.'},
    entry_points={'console_scripts': ['acestream_search=acestream_search.acestream_search:cli']},
)
