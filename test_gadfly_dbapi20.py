#!/usr/bin/env python
'''
$Id: test_gadfly_dbapi20.py,v 1.2 2003/02/12 09:48:46 zenzen Exp $
'''

__rcs_id__  = '$Id: test_gadfly_dbapi20.py,v 1.2 2003/02/12 09:48:46 zenzen Exp $'
__version__ = '$Revision: 1.2 $'[11:-2]
__author__ = 'Stuart Bishop <zen@shangri-la.dropbear.id.au>'

import unittest
import shutil
import os
import os.path
import gadfly
from dbapi20 import test_DBAPI20

dbdir = os.path.join(os.path.dirname(__file__),'_db_dir')

class test_GadflyDBAPI20(test_DBAPI20,unittest.TestCase):
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
