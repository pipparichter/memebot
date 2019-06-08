import setuptools
from Cython.build import cythonize

with README.txt as r:
    long_description = r.read()    

setuptools.setup(
        zip_safe = False,
        name = 'HoeBot', 
        description = 'GroupMe bot',
        long_description = long_description
        author = 'Philippa Richter',
        author_email = 'philippa.a.richter@gmail.com',
        py_modules = ['Hoebot.py', 'gloal_vars.py', 'meme_lib.py' ]
        ext_modules = [cythonize('yeeter_meter.pyx'), cythonize('triggers.pyx')],
        install_requires = ['certifi', 'chardet', 'idna', 'requests', 'urllib3', 'gunicorn']
        )
