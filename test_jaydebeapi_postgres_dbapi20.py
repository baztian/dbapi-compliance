#!/usr/bin/env python

# Test suite driver for JayDeBeApi using postgresql JDBC driver

import dbapi20
import unittest
import popen2
import getpass

import jaydebeapi

class test_JayDeBeApiPostgres(dbapi20.DatabaseAPI20Test):
    driver = jaydebeapi
    connect_args = ('org.postgresql.Driver', ['jdbc:postgresql:dbapi20_test',
                                              getpass.getuser(), ''])
    connect_kw_args = { }

    lower_func = 'lower' # For stored procedure test

    def _connect(self):
        c = dbapi20.DatabaseAPI20Test._connect(self)
        c.jconn.setAutoCommit(False)
        return c
    def executeDDL1(self, cursor):
        cursor.execute(self.ddl1)
    def setUp(self):
        # Call superclass setUp In case this does something in the
        # future
        dbapi20.DatabaseAPI20Test.setUp(self)

        try:
            con = self._connect()
            con.close()
        except:
            cmd = "psql -c 'create database dbapi20_test'"
            cout,cin = popen2.popen2(cmd)
            cin.close()
            cout.read()

    def tearDown(self):
        dbapi20.DatabaseAPI20Test.tearDown(self)

    def test_nextset(self): pass
    def test_setoutputsize(self): pass

if __name__ == '__main__':
    unittest.main()
