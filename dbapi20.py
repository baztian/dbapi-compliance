#!/usr/bin/env python
'''
$Id: dbapi20.py,v 1.2 2003/02/12 09:48:46 zenzen Exp $
'''

__rcs_id__  = '$Id: dbapi20.py,v 1.2 2003/02/12 09:48:46 zenzen Exp $'
__version__ = '$Revision: 1.2 $'[11:-2]
__author__ = 'Stuart Bishop <zen@shangri-la.dropbear.id.au>'

import unittest

class test_DBAPI20:
    ''' Test a database self.driver for DB API 2.0 compatibility.
        This implementation tests Gadfly, but the TestCase
        is structured so that other self.drivers can subclass this 
        test case to ensure compiliance with the DB-API. It is 
        expected that this TestCase may be expanded in the future
        if ambiguities or edge conditions are discovered.

        The 'Optional Extensions' are not yet being tested.

        self.drivers should subclass this test, overriding setUp, tearDown,
        self.driver, connect_args and connect_kw_args. Class specification
        should be as follows:
        import dbapi20
        class mytest(dbapi20.test_DBAPI20,unittest.TestCase):
           [...] 
    '''

    # The self.driver module. This should be the module where the 'connect'
    # method is to be found
    driver = None
    connect_args = () # List of arguments to pass to connect
    connect_kw_args = {} # Keyword arguments for connect

    ddl1 = 'create table booze (name varchar)'
    ddl2 = 'create table barflys (name varchar)'
    xddl1 = 'drop table booze'
    xddl2 = 'drop table barflys'
        
    def setUp(self):
        ''' self.drivers should override this method to perform required setup
            if any is necessary, such as creating the database.
        '''
        pass

    def tearDown(self):
        ''' self.drivers should override this method to perform required cleanup
            if any is necessary, such as deleting the dest database.
        '''
        con = self._connect()
        try:
            cur = con.cursor()
            for ddl in (self.xddl1,self.xddl2):
                try: 
                    cur.execute(ddl)
                except self.driver.Error: 
                    # Assume table didn't exist. Other tests will check if
                    # execute is busted.
                    pass
        finally:
            con.close()

    def _connect(self):
        try:
            return self.driver.connect(
                *self.connect_args,**self.connect_kw_args
                )
        except AttributeError:
            self.fail("No connect method found in self.driver module")

    def test_connect(self):
        con = self._connect()
        con.close()

    def test_apilevel(self):
        try:
            apilevel = self.driver.apilevel
            self.assertEqual(apilevel,'2.0')
        except AttributeError:
            self.fail("Driver doesn't define apilevel")

    def test_threadsafety(self):
        try:
            threadsafety = self.driver.threadsafety
            self.failUnless(threadsafety in (0,1,2,3))
        except AttributeError:
            self.fail("Driver doesn't define threadsafety")

    def test_paramstyle(self):
        try:
            paramstyle = self.driver.paramstyle
            self.failUnless(paramstyle in (
                'qmark','numeric','named','format','pyformat'
                ))
        except AttributeError:
            self.fail("Driver doesn't define paramstyle")

    def test_Exceptions(self):
        self.failUnless(issubclass(self.driver.Warning,StandardError))
        self.failUnless(issubclass(self.driver.Error,StandardError))
        self.failUnless(issubclass(self.driver.InterfaceError,StandardError))
        self.failUnless(issubclass(self.driver.DatabaseError,StandardError))
        self.failUnless(issubclass(self.driver.OperationalError,StandardError))
        self.failUnless(issubclass(self.driver.IntegrityError,StandardError))
        self.failUnless(issubclass(self.driver.InternalError,StandardError))
        self.failUnless(issubclass(self.driver.ProgrammingError,StandardError))
        self.failUnless(issubclass(self.driver.NotSupportedError,StandardError))

    def test_commit(self):
        con = self._connect()
        try:
            con.commit()
        finally:
            con.close()

    def test_rollback(self):
        con = self._connect()
        if hasattr(con,'rollback'):
            try:
                con.rollback()
            except NotSupportedError:
                pass
    
    def test_cursor(self):
        con = self._connect()
        try:
            cur = con.cursor()
        finally:
            con.close()

    def test_cursor_isolation(self):
        con = self._connect()
        try:
            cur1 = con.cursor()
            cur2 = con.cursor()
            cur1.execute(self.ddl1)
            cur1.execute("insert into booze values ('Victoria Bitter')")
            cur2.execute("select name from booze")
            booze = cur2.fetchall()
            self.assertEqual(len(booze),1)
            self.assertEqual(len(booze[0]),1)
            self.assertEqual(booze[0][0],'Victoria Bitter')
        finally:
            con.close()

    def test_description(self):
        con = self._connect()
        try:
            cur = con.cursor()
            cur.execute(self.ddl1)
            self.assertEqual(cur.description,None)
            cur.execute('select name from booze')
            self.assertEqual(len(cur.description),1)
            self.assertEqual(len(cur.description[0]),7)
            self.assertEqual(cur.description[0][0].lower(),'name')
            self.failIfEqual(cur.description[0][1],self.driver.STRING)

            # Make sure self.description gets reset
            cur.execute(self.ddl2)
            self.assertEqual(cur.description,None)
        finally:
            con.close()

    def test_rowcount(self):
        con = self._connect()
        try:
            cur = con.cursor()
            cur.execute(self.ddl1)
            self.assertEqual(cur.rowcount,-1)
            cur.execute("insert into booze values ('Victoria Bitter')")
            self.failUnless(cur.rowcount in (-1,1))
            cur.execute("select name from booze")
            self.failUnless(cur.rowcount in (-1,1))
            cur.execute(ddl2)
            self.assertEqual(cur.rowcount,-1)
        finally:
            con.close()

    def test_callproc(self):
        # Cannot write a generic test. self.driver's implementations of this
        # TestCase should implement this test. self.drivers that don't support
        # stored procedures should just 'pass'
        raise NotImplementedError,'Driver testcase should override this test'

    def test_close(self):
        con = self._connect()
        try:
            cur = con.cursor()
        finally:
            con.close()
        self.assertRaises(self.driver.Error,cur.execute,self.ddl1)
        self.assertRaises(self.driver.Error,con.commit)
        self.assertRaises(self.driver.Error,con.close)

    def test_execute(self):
        con = self._connect()
        try:
            cur = con.cursor()
            self._paraminsert(cur)
        finally:
            con.close()

    def _paraminsert(self,cur):
        cur.execute(self.ddl1)
        cur.execute("insert into booze values ('Victoria Bitter')")
        if self.driver.paramstyle == 'qmark':
            cur.execute('insert into booze values (?)',("Cooper's",))
        elif self.driver.paramstyle == 'numeric':
            cur.execute('insert into booze values (:1)',("Cooper's",))
        elif self.driver.paramstyle == 'named':
            cur.execute(
                'insert into booze values (:beer)', {'beer':"Cooper's"}
                )
        elif self.driver.paramstyle == 'format':
            cur.execute('insert into booze values (%s)',("Cooper's",))
        elif self.driver.paramstyle == 'pyformat':
            cur.execute(
                'insert into booze values (%(beer)s)',{'beer':"Cooper's"}
                )
        else:
            self.fail('Unknown paramstyle')
        cur.execute('select name from booze')
        res = cur.fetchall()
        self.assertEqual(len(res),2)
        beers = [res[0][0],res[1][0]]
        beers.sort()
        self.assertEqual(beers[0],"Cooper's")
        self.assertEqual(beers[1],"Victoria Bitter")

    def test_executemany(self):
        con = self._connect()
        try:
            cur = con.cursor()
            cur.execute(self.ddl1)
            largs = [ ("Cooper's",) , ("Boag's",) ]
            margs = [ {'beer': "Cooper's"}, {'beer': "Boag's"} ]
            if self.driver.paramstyle == 'qmark':
                cur.executemany('insert into booze values (?)',largs)
            elif self.driver.paramstyle == 'numeric':
                cur.executemany('insert into booze values (:1)',largs)
            elif self.driver.paramstyle == 'named':
                cur.executemany('insert into booze values (:beer)',margs)
            elif self.driver.paramstyle == 'format':
                cur.executemany('insert into booze values (%s)',largs)
            elif self.driver.paramstyle == 'pyformat':
                cur.executemany('insert into booze values (%(beer)s)',margs)
            else:
                self.fail('Unknown paramstyle')
            cur.execute('select name from booze')
            res = cur.fetchall()
            self.assertEqual(len(res),2)
            beers = [res[0][0],res[1][0]]
            beers.sort()
            self.assertEqual(beers[0],"Boag's")
            self.assertEqual(beers[1],"Cooper's")
        finally:
            con.close()

    def test_fetchone(self):
        con = self._connect()
        try:
            cur = con.cursor()
            self.assertRaises(self.driver.Error,cur.fetchone)
            cur.execute(self.ddl1)
            self.assertRaises(self.driver.Error,cur.fetchone)
            cur.execute("insert into booze values ('Victoria Bitter')")
            self.assertRaises(self.driver.Error,cur.fetchone)
            cur.execute('select name from booze')
            r = cur.fetchone()
            self.assertEqual(len(r),1)
            self.assertEqual(r[0],'Victoria Bitter')
            self.assertEqual(cur.fetchone(),None)
        finally:
            con.close()

    samples = [
        'Carlton Cold',
        'Carlton Draft',
        'Mountain Goat',
        'Redback',
        'Victoria Bitter',
        'XXXX'
        ]

    populate = [ddl1,] +  \
        ["insert into booze values ('%s')" % s for s in samples]

    def test_fetchmany(self):
        con = self._connect()
        try:
            cur = con.cursor()

            self.assertRaises(self.driver.Error,cur.fetchmany,size=4)

            for sql in self.populate:
                cur.execute(sql)

            cur.arraysize=10
            cur.execute('select name from booze')
            r = cur.fetchmany(4) # Should get 4 rows
            self.assertEqual(len(r),4)
            r = cur.fetchmany(4) # Should get 2 more
            self.assertEqual(len(r),2)
            r = cur.fetchmany(4) # Should be an empty sequence
            self.assertEqual(len(r),0)

            cur.execute('select name from booze')
            r = cur.fetchmany(size=4) # Should get 4 rows
            self.assertEqual(len(r),4)
            r = cur.fetchmany(size=1) # Should get 1 more
            self.assertEqual(len(r),1)
            r = cur.fetchmany(size=4) # Should get 1 more
            self.assertEqual(len(r),1)
            r = cur.fetchmany(size=4) # Should get an empty sequence
            self.assertEqual(len(r),0)

            cur.arraysize=4
            cur.execute('select name from booze')
            r = cur.fetchmany() # Should get 4 rows
            self.assertEqual(len(r),4)
            r = cur.fetchmany() # Should get 2 more
            self.assertEqual(len(r),2)
            r = cur.fetchmany() # Should be an empty sequence
            self.assertEqual(len(r),0)

            cur.arraysize=6
            cur.execute('select name from booze')
            rows = cur.fetchmany() # Should get all rows
            self.assertEqual(len(r),6)
            self.assertEqual(len(r),6)
            rows = [r[0] for r in rows]
            rows.sort()
          
            # Make sure we get the right data back out
            for i in range(0,6):
                self.assertEqual(rows[i],self.samples[i])

            cur.execute(self.ddl2)
            cur.execute('select name from barflys')
            r = cur.fetchmany() # Should get empty sequence
            self.assertEqual(len(r),0)

        finally:
            con.close()

    def test_fetchall(self):
        con = self._connect()
        try:
            cur = con.cursor()
            self.assertRaises(self.driver.Error,cur.fetchall)

            for sql in self.populate:
                cur.execute(sql)
            self.assertRaises(self.driver.Error,cur.fetchall)

            cur.execute('select name from booze')
            rows = cur.fetchall()
            self.assertEqual(len(rows),len(self.samples))
            rows = [r[0] for r in rows]
            rows.sort()
            for i in range(0,len(self.samples)):
                self.assertEqual(rows[i],self.samples[i])

            cur.execute(self.ddl2)
            cur.execute('select name from barflys')
            rows = cur.fetchall()
            self.assertEqual(len(rows),0)
            
        finally:
            con.close()
    
    def test_mixedfetch(self):
        con = self._connect()
        try:
            cur = con.cursor()
            for sql in self.populate:
                cur.execute(sql)

            cur.execute('select name from booze')
            rows1  = cur.fetchone()
            rows23 = cur.fetchmany(2)
            rows4  = cur.fetchone()
            rows56 = cur.fetchall()
            self.assertEqual(len(rows23),2)
            self.assertEqual(len(rows56),2)

            rows = [rows1[0]]
            rows.extend([rows23[0][0],rows23[1][0]])
            rows.append(rows4[0])
            rows.extend([rows56[0][0],rows56[1][0]])
            rows.sort()
            for i in range(0,len(self.samples)):
                self.assertEqual(rows[i],self.samples[i])
        finally:
            con.close()

    def test_nextset(self):
        raise NotImplementedError,'Drivers need to override this test'

    def test_arraysize(self):
        # Not much here - rest of the tests for this are in test_fetchmany
        con = self._connect()
        try:
            cur = con.cursor()
            self.failUnless(hasattr(cur,'arraysize'))
        finally:
            con.close()

    def test_setinputsizes(self):
        con = self._connect()
        try:
            cur = con.cursor()
            cur.execute(self.ddl1)
            cur.setinputsizes( (25,) )
            self._paraminsert(cur)
        finally:
            con.close()

    def test_setoutputsize_basic(self):
        # Basic test is to make sure it doesn't blow up
        con = self._connect()
        try:
            cur = con.cursor()
            cur.execute(self.ddl1)
            cur.setoutputsize(1000)
            self._paraminsert(cur)
        finally:
            con.close()

    def test_setoutputsize(self):
        # Real test for setoutputsize is driver dependant
        raise NotImplementedError,'Driver need to override this test'

    def test_Date(self):
        d1 = self.driver.Date(2002,12,25)
        d2 = self.driver.DateFromTicks(1040823930)
        # Can we assume this? API doesn't specify, but it seems implied
        self.assertEqual(str(d1),str(d2))

    def test_Time(self):
        t1 = self.driver.Time(13,45,30)
        t2 = self.driver.TimeFromTicks(1040823930)
        # Can we assume this? API doesn't specify, but it seems implied
        self.assertEqual(str(t1),str(t2))

    def test_Timestamp(self):
        t1 = self.driver.Timestamp(2002,12,25,13,45,30)
        t2 = self.driver.TimestampFromTicks(1040823930)
        # Can we assume this? API doesn't specify, but it seems implied
        self.assertEqual(str(t1),str(t2))

    def test_Binary(self):
        b = self.driver.Binary('Something')
        b = self.driver.Binary('')

    def test_STRING(self):
        self.failUnless(hasattr(self.driver,'STRING'))

    def test_BINARY(self):
        self.failUnless(hasattr(self.driver,'BINARY'))

    def test_NUMBER(self):
        self.failUnless(hasattr(self.driver,'NUMBER'))

    def test_DATETIME(self):
        self.failUnless(hasattr(self.driver,'DATETIME'))

    def test_ROWID(self):
        self.failUnless(hasattr(self.driver,'ROWID'))

