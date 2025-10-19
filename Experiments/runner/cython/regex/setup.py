# setup.py
from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "regex_cy",
        ["regex_cy.pyx"],
        extra_compile_args=['-O3'],
    )
]

setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
        }
    )
)