from setuptools import setup

setup(
    name='dbapi-compliance',
    version='1.15.0',
    description='Python DB API 2.0 driver compliance unit test suite.',
    long_description=open('README.rst').read(),
    url='https://github.com/baztian/dbapi-compliance',
    license='PD',
    author='Stuart Bishop',
    author_email='stuart@stuartbishop.net',
    py_modules=['dbapi20'],
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
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
