#!/usr/bin/env python2

# If installing in Python 2, standard Distutils is enough.
# If installing in Python 3, Distribute is needed for the 2to3 conversion.
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'FEbabel',
    version = '0.0.0',
    description = 'Read and write a variety of finite element input formats',
    long_description = open('README.rst').read(),
    author = 'Randy Heydon',
    author_email = 'randy.heydon@clockworklab.net',
    license = 'CC:BY-SA',

    packages = ['febabel', 'febabel._formats'],
    scripts = ['translateFE'],
    test_suite = 'test',
    use_2to3 = True,
)
