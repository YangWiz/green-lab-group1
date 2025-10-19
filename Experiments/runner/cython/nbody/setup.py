# setup.py
from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "nbody_cy",
        ["nbody_cy.pyx"],
        extra_compile_args=['-O3', '-ffast-math'],
    )
]

setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
            'cdivision': True,
        }
    )
)