from setuptools import setup
import versioneer
zip_safe = False
setup(
    name='acestream_search',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=['acestream_search'],
    package_dir={'acestream_search': '.'},
    entry_points={'console_scripts': ['acestream_search=acestream_search.acestream_search:cli']},
)
