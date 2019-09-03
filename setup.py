from setuptools import setup, find_packages

setup(
    name='acestream_search',
    version='1.0.2',
    packages=['acestream_search'],
    package_dir={'acestream_search': '.'},
    entry_points={'console_scripts': ['acestream_search=acestream_search.acestream_search:main']},
    test_suite='test_search'
)
