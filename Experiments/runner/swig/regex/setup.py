# setup.py for SWIG regex tokenizer
from setuptools import setup, Extension

regex_module = Extension(
    '_regex_swig',
    sources=['regex_swig.i', 'regex_swig.cpp'],
    swig_opts=['-c++'],
    extra_compile_args=['-O3', '-std=c++11'],
)

setup(
    name='regex_swig',
    ext_modules=[regex_module],
    py_modules=['regex_swig'],
)