# setup.py for SWIG matrix multiplication
from setuptools import setup, Extension

matmul_module = Extension(
    '_matmul_swig',
    sources=['matmul_swig.i', 'matmul_swig.cpp'],
    swig_opts=['-c++'],
    extra_compile_args=['-O3', '-std=c++11', '-ffast-math'],
)

setup(
    name='matmul_swig',
    ext_modules=[matmul_module],
    py_modules=['matmul_swig'],
)