from os import environ, remove
from os.path import dirname, join, isfile
from distutils.core import setup
from distutils.extension import Extension
try:
    from Cython.Build import cythonize
    from Cython.Distutils import build_ext
    have_cython = True
except ImportError:
    have_cython = False
import sys

platform = sys.platform
if platform == 'win32':
	cstdarg = '-std=gnu99'
else:
	cstdarg = '-std=c99'

do_clear_existing = True



parallax_modules = {
    'parallax_module.parallax': ['modules/parallax/parallax.pyx',],
    'parallax_module.position': ['modules/parallax/position.pyx',],
    }

parallax_modules_c = {
    'parallax_module.parallax': ['modules/parallax/parallax.c',],
    'parallax_module.position': ['modules/parallax/position.c',],
    }

check_for_removal = ['modules/parallax/parallax.c', 'modules/parallax/position.c']

def build_ext(ext_name, files, include_dirs=[]):
    return Extension(ext_name, files, include_dirs,
        extra_compile_args=[cstdarg, '-ffast-math',])

extensions = []
parallax_extensions = []
cmdclass = {}

def build_extensions_for_modules_cython(ext_list, modules):
    ext_a = ext_list.append
    for module_name in modules:
        ext = build_ext(module_name, modules[module_name])
        if environ.get('READTHEDOCS', None) == 'True':
            ext.pyrex_directives = {'embedsignature': True}
        ext_a(ext)
    return cythonize(ext_list)

def build_extensions_for_modules(ext_list, modules):
    ext_a = ext_list.append
    for module_name in modules:
        ext = build_ext(module_name, modules[module_name])
        if environ.get('READTHEDOCS', None) == 'True':
            ext.pyrex_directives = {'embedsignature': True}
        ext_a(ext)
    return ext_list

if have_cython:
    if do_clear_existing:
        for file_name in check_for_removal:
            if isfile(file_name):
                remove(file_name)
    parallax_extensions = build_extensions_for_modules_cython(
        parallax_extensions, parallax_modules)
else:
    parallax_extensions = build_extensions_for_modules(parallax_extensions, 
        parallax_modules_c)

setup(
    name='KivEnt Parallax Module',
    description='''Handling the parallax effect''',
    author='sireliah',
    author_email='pgolabb@gmail.com',
    ext_modules=parallax_extensions,
    cmdclass=cmdclass,
    packages=[
        'parallax_module',
        ],
    package_dir={'parallax_module': 'modules/parallax'})
