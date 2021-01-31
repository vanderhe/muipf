#!/usr/bin/env python3
from distutils.core import setup


setup(
    name='MUIPF',
    version='0.1',
    description='Mutual Information Image Processing Framework',
    author='Tammo van der Heide, Steffen Wilksen',
    url='https://github.com/vanderhe/muipf',
    platforms='platform independent',
    package_dir={'': 'src'},
    packages=['muipf', 'muipf.scripts'],
    scripts=[
        'bin/picslide',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
    ],
    long_description='''
Mutual Information Image Processing Framework
-----------------------------------------
MUIPF is a minimalistic software package to perform image
processing based on mutual information, written in Python.
Currently, only the functionality for sliding two images
on top of each other is implemented.
''',
    requires=['numpy']
)
