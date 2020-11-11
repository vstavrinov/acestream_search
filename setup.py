from setuptools import setup, find_packages
import versioneer

with open('README.md', 'r') as f:
    long_description = f.read()

zip_safe = False
setup(
    name='acestream_search',
    description='Produces acestream m3u playlist, xml epg or json data.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/vstavrinov/acestream_search',
    author='Vladimir Stavrinov',
    author_email='vstavrinov@gmail.com',
    license='GNU General Public License v3 (GPLv3)',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    entry_points={'console_scripts': ['acestream_search=acestream_search.acestream_search:cli']},
    install_requires=['lxml'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Environment :: Console',
                 'Intended Audience :: End Users/Desktop',
                 'Operating System :: POSIX',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: MacOS',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9',
                 'Topic :: Internet :: WWW/HTTP',
                 'Topic :: Multimedia :: Video',
                 'Topic :: Utilities']
)
