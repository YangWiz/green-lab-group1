# setup.py for SWIG convolution
from setuptools import setup, Extension

conv_module = Extension(
    '_conv_swig',
    sources=['conv_swig.i', 'conv_swig.cpp'],
    swig_opts=['-c++'],
    extra_compile_args=['-O3', '-std=c++11', '-ffast-math'],
)

setup(
    name='conv_swig',
    ext_modules=[conv_module],
    py_modules=['conv_swig'],
)