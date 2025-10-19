# setup.py for SWIG quicksort
from setuptools import setup, Extension

quicksort_module = Extension(
    '_quicksort_swig',
    sources=['quicksort_swig.i', 'quicksort_swig.cpp'],
    swig_opts=['-c++'],
    extra_compile_args=['-O3', '-std=c++11'],
)

setup(
    name='quicksort_swig',
    ext_modules=[quicksort_module],
    py_modules=['quicksort_swig'],
)