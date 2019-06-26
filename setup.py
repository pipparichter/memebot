import setuptools
# from setuptools.extension import Extension
# from Cython.Build import cythonize

with open('README.md', 'r') as R:
    long_description = R.read()    

setuptools.setup(
        zip_safe = False,
       
        name = 'memebot', 
        description = 'GroupMe bot',
        long_description = long_description,
        author = 'Philippa Richter',
        author_email = 'philippa.a.richter@gmail.com',

        packages = {
            'memebot':['.*py'], 
            'memebot.features':['.*py', '.*pyx'], 
            'memebot.dictionaries':['.*py']},
        
        # ext_modules = [
            # cythonize('./memebot/features/word_counter.pyx'),
            # cythonize('./memebot/bot_reply.pyx'),
            # cythonize('./memebot/features/meme_generator.pyx')],
        
        install_requires = open('requirements.txt', 'r').read().split('\n'),

        )
