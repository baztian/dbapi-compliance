#!/usr/bin/env python
'''
$Id: test_gadfly_dbapi20.py,v 1.1 2003/02/11 15:09:17 zenzen Exp $
'''

__rcs_id__  = '$Id: test_gadfly_dbapi20.py,v 1.1 2003/02/11 15:09:17 zenzen Exp $'
__version__ = '$Revision: 1.1 $'[11:-2]
__author__ = 'Stuart Bishop <zen@shangri-la.dropbear.id.au>'

import unittest
import gadfly
from dbapi20 import test_DBAPI20

class test_GadflyDBAPI20(test_DBAPI20,unittest.TestCase):
    driver_module = gadfly

    def test_callproc(self): pass
    def test_nextset(self): pass
    def test_setoutputsize(self): pass
