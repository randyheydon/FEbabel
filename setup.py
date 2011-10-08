#!/usr/bin/env python2
from distutils.core import setup

setup(
    name = 'FEbabel',
    version = '0.0.0',
    description = 'Read and write a variety of finite element input formats',
    long_description = open('README.rst').read(),
    author = 'Randy Heydon',
    author_email = 'randy.heydon@clockworklab.net',
    packages = ['febabel'],
    scripts = 'translateFE',
    license = 'CC:BY-SA',
)
