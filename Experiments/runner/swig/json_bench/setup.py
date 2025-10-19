# setup.py for SWIG JSON helpers
from setuptools import setup, Extension

json_module = Extension(
    '_json_swig',
    sources=['json_swig.i', 'json_swig.cpp'],
    swig_opts=['-c++'],
    extra_compile_args=['-O3', '-std=c++11'],
)

setup(
    name='json_swig',
    ext_modules=[json_module],
    py_modules=['json_swig'],
)