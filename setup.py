from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy

ext = Extension(name="cca", sources=["cca.pyx"])
setup(ext_modules=cythonize(ext),
      include_dirs=[numpy.get_include()])
