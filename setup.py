import os

from setuptools import setup

setup(
    name='dbapi20',
    version='1.14.3',
    description='Python DB API 2.0 driver compliance unit test suite.',
    url='https://github.com/baztian/dbapi-compliance',
    license='PD',
    author='Stuart Bishop',
    author_email='stuart@stuartbishop.net',
    py_modules=['dbapi2'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
