#!/usr/bin/env python
'''
$Id: test_gadfly_dbapi20.py,v 1.3 2003/09/17 03:23:14 zenzen Exp $
'''

__rcs_id__  = '$Id: test_gadfly_dbapi20.py,v 1.3 2003/09/17 03:23:14 zenzen Exp $'
__version__ = '$Revision: 1.3 $'[11:-2]
__author__ = 'Stuart Bishop <zen@shangri-la.dropbear.id.au>'

import unittest
import shutil
import os
import os.path
import gadfly
import dbapi20

dbdir = os.path.join(os.path.dirname(__file__),'_db_dir')

class test_GadflyDBAPI20(dbapi20.DatabaseAPI20Test):
    driver = gadfly
    connect_kw_args = {'dbname': 'test','dbdir': dbdir}

    def setUp(self):
        if os.path.exists(dbdir):
            shutil.rmtree(dbdir)
        os.makedirs(dbdir)

    def tearDown(self):
        if os.path.exists(dbdir):
            shutil.rmtree(dbdir)

    def test_callproc(self): pass
    def test_nextset(self): pass
    def test_setoutputsize(self): pass

if __name__ == '__main__':
    unittest.main()
