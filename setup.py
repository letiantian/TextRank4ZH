# -*- coding: utf-8 -*-
from distutils.core import setup
LONGDOC = """
Please go to https://github.com/someus/TextRank4ZH for more info.
"""

setup(
    name='textrank4zh',
    version='0.3',
    description='Extract keywords and abstract Chinese article',
    long_description=LONGDOC,
    author='Letian Sun',
    author_email='sunlt1699@gmail.com',
    url='https://github.com/someus/TextRank4ZH',
    license="MIT",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Chinese (Traditional)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='NLP,Chinese,Keywords extraction, Abstract extraction',
    install_requires=['jieba >= 0.35', 'numpy >= 1.7.1', 'networkx >= 1.9.1'],
    packages=['textrank4zh'],
    package_dir={'textrank4zh':'textrank4zh'},
    package_data={'textrank4zh':['*.txt',]},
)