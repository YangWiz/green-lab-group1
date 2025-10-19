# setup.py for SWIG FFT
from setuptools import setup, Extension

fft_module = Extension(
    '_fft_swig',
    sources=['fft_swig.i', 'fft_swig.cpp'],
    swig_opts=['-c++'],
    extra_compile_args=['-O3', '-std=c++11', '-ffast-math'],
)

setup(
    name='fft_swig',
    ext_modules=[fft_module],
    py_modules=['fft_swig'],
)