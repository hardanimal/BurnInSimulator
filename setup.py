#!/usr/bin/env python
# encoding: utf-8
#import codecs
#try:
#    codecs.lookup('mbcs')
#except LookupError:
#    ascii = codecs.lookup('ascii')
#    func = lambda name, enc=ascii: {True: enc}.get(name == 'mbcs')
#    codecs.register(func)

from src import BIS
from src import BIS_GUI
from setuptools import setup

#from distutils.core import setup

setup(
    name="BurnIn_Simulator",
    version=BIS.__version__,
    package_dir={'': 'src'},
    packages=["BIS",
              "BIS_GUI"],
    package_data={'': ['*.xml', '*.dll', '*.so']},
    author="danzel.li",
    description='II-VI Burnin Simulator',
    platforms="any",
    entry_points={
        "console_scripts": [
            'bis = BIS_GUI.main:start'
        ]
    }
)
