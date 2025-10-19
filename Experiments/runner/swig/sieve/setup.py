# setup.py for SWIG sieve
from setuptools import setup, Extension

sieve_module = Extension(
    '_sieve_swig',
    sources=['sieve_swig.i', 'sieve_swig.cpp'],
    swig_opts=['-c++'],
    extra_compile_args=['-O3', '-std=c++11'],
)

setup(
    name='sieve_swig',
    ext_modules=[sieve_module],
    py_modules=['sieve_swig'],
)