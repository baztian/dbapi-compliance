#!/usr/bin/env python
'''
$Id: test_gadfly_dbapi20.py,v 1.5 2003/10/02 16:41:01 moellenbeck Exp $
'''

__rcs_id__  = '$Id: test_gadfly_dbapi20.py,v 1.5 2003/10/02 16:41:01 moellenbeck Exp $'
__version__ = '$Revision: 1.5 $'[11:-2]
__author__ = 'Stuart Bishop <zen@shangri-la.dropbear.id.au>'

import unittest
import shutil
import os
import os.path
import gadfly
import dbapi20

#dbdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'_db_dir'))
dbdir = os.path.abspath(os.path.join(".",'_db_dir'))

class test_GadflyDBAPI20(dbapi20.DatabaseAPI20Test):
    driver = gadfly
    connect_kw_args = {'databasename': 'test', 'directory': dbdir}

    def setUp(self):
        if os.path.exists(dbdir):
            shutil.rmtree(dbdir)
        os.makedirs(dbdir)
        g = gadfly.gadfly()
        g.startup(self.connect_kw_args['databasename'],
                  self.connect_kw_args['directory'])
        c = g.cursor()
        c.execute("select * from __table_names__")
        c.execute("create table ph (nm varchar, ph varchar)")
        g.commit()

    def tearDown(self):
        if os.path.exists(dbdir):
            shutil.rmtree(dbdir)

    def test_None(self):
        # gadfly parser does'nt understand NULL
        pass

    def test_description(self):
        # only when the select-execute return an result, the types of the 
        # description can determinat (see: gadfly/database.py line 390 ...)
        pass
            
    def test_callproc(self): pass
    def test_nextset(self): pass
    def test_setoutputsize(self): pass

if __name__ == '__main__':
    unittest.main()
