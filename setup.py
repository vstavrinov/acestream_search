from setuptools import setup
zip_safe = False
setup(
    name='acestream_search',
    version='1.1.1',
    packages=['acestream_search'],
    package_dir={'acestream_search': '.'},
    entry_points={'console_scripts': ['acestream_search=acestream_search.acestream_search:main']},
)
