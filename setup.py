import setuptools
from setuptools.extension import Extension
from Cython.Build import cythonize

with open('README.md', 'r') as R:
    long_description = R.read()    

setuptools.setup(
       
        name = 'memebot', 
        description = 'GroupMe bot',
        long_description = long_description,
        author = 'Philippa Richter',
        author_email = 'philippa.a.richter@gmail.com',

        packages = {
            'memebot':['.*py'], 
            'memebot.features':['.*py', '.*pyx'], 
            'memebot.dictionaries':['.*py']},
        
        ext_modules = [
            cythonize('./features/word_counter.pyx'),
            cythonize('./bot_reply.pyx'),
            cythonize('./features/meme_generator.pyx')],
        
        install_requires = ['cython', 'certifi', 'chardet', 'idna', 'requests', 'urllib3', 'gunicorn'],
        
        zip_safe = False
        )
