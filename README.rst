=========================================
 The Python DB-API Compliance Test Suite
=========================================

.. image:: https://img.shields.io/travis/baztian/dbapi-compliance/master.svg
   :target: https://travis-ci.org/baztian/dbapi-compliance

.. image:: https://img.shields.io/badge/python-2.6,_2.7,_3.3,_3.4-blue.svg
    :target: https://pypi.python.org/pypi/dbapi-compliance/

.. image:: https://img.shields.io/github/tag/baztian/dbapi-compliance.svg
    :target: https://pypi.python.org/pypi/dbapi-compliance/

.. image:: https://img.shields.io/pypi/dm/dbapi-compliance.svg
    :target: https://pypi.python.org/pypi/dbapi-compliance/

A unit test suite to help confirm that Python database drivers conform
to the Python DB-API_ specification v2.0.

License
=======

dbapi-compliance is released in the public domain.

Changelog
=========

- Next version - unreleased
- 1.15.0 - 2015-07-04

  - Apply fix to no-result statement check in test_rowcount being too
    strict.

  - Fix parameter substitution being mixed.

  - Fix for non idempotent close.

  - Fix psycopg2 test not being Python 3 compatible.

  - Make it possible to customize insert statements (thanks
    @lalinsky).

  - Support databases that require primary keys being non null (thanks
    @lalinsky).

  - Build on travis.

  - Provide PyPI package (thanks @lalinsky for the setup.py fixes).

  - Use bumpversion.

- 1.14.3 - 2013-06-05 and earlier

  - Initial implementation by Stuart Bishop.

  - Python 3 compatibility by Vernon Cole.

.. _DB-API: http://www.python.org/dev/peps/pep-0249/
