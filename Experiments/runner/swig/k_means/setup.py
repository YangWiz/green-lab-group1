# setup.py for SWIG K-means
from setuptools import setup, Extension

kmeans_module = Extension(
    '_kmeans_swig',
    sources=['kmeans_swig.i', 'kmeans_swig.cpp'],
    swig_opts=['-c++'],
    extra_compile_args=['-O3', '-std=c++11', '-ffast-math'],
)

setup(
    name='kmeans_swig',
    ext_modules=[kmeans_module],
    py_modules=['kmeans_swig'],
)