# setup.py for SWIG N-body
from setuptools import setup, Extension

nbody_module = Extension(
    '_nbody_swig',
    sources=['nbody_swig.i', 'nbody_swig.cpp'],
    swig_opts=['-c++'],
    extra_compile_args=['-O3', '-std=c++11', '-ffast-math'],
)

setup(
    name='nbody_swig',
    ext_modules=[nbody_module],
    py_modules=['nbody_swig'],
)