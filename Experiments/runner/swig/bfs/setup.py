# setup.py for SWIG BFS
from setuptools import setup, Extension

bfs_module = Extension(
    '_bfs_swig',
    sources=['bfs_swig.i', 'bfs_swig.cpp'],
    swig_opts=['-c++'],
    extra_compile_args=['-O3', '-std=c++11'],
)

setup(
    name='bfs_swig',
    ext_modules=[bfs_module],
    py_modules=['bfs_swig'],
)