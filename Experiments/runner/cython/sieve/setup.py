# setup.py
from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize(
        "sieve_cy.pyx",
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
            'cdivision': True
        }
    ),
    include_dirs=[numpy.get_include()]
)