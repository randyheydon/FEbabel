#!/usr/bin/env python2
import unittest

import sys, os
# For Python 3, use the translated version of the library.
# For Python 2, find the library one directory up.
if sys.version < '3':
    sys.path.append(os.path.dirname(sys.path[0]))
from febabel import constraints as con


class TestConstraint(unittest.TestCase):


    def test_init(self):
        force = con.Force(con.loadcurve_ramp, 75)
        disp = con.Displacement(con.LoadCurve({0:0, 0.5:50, 1:51}))
        fix = con.fixed



class TestSwitch(unittest.TestCase):


    def test_get_active(self):
        f1 = con.Displacement(con.loadcurve_ramp, -10)
        f2 = con.fixed
        f3 = con.Force(con.loadcurve_constant, 100)
        f4 = con.free
        s = con.SwitchConstraint({0:f1, 1:f2, 1.1:f3, 1.2:f4})
        self.assertTrue( s.get_active(-0.2) is None )
        self.assertTrue( s.get_active(0) is f1 )
        self.assertTrue( s.get_active(0.2) is f1 )
        self.assertTrue( s.get_active(0.999) is f1 )
        self.assertTrue( s.get_active(1) is f2 )
        self.assertTrue( s.get_active(1.0) is f2 )
        self.assertTrue( s.get_active(1.01) is f2 )
        self.assertTrue( s.get_active(1.0999) is f2 )
        self.assertTrue( s.get_active(1.1) is f3 )
        self.assertTrue( s.get_active(1.11) is f3 )
        self.assertTrue( s.get_active(1.1999) is f3 )
        self.assertTrue( s.get_active(1.2) is f4 )
        self.assertTrue( s.get_active(1.201) is f4 )
        self.assertTrue( s.get_active(1.5) is f4 )
        self.assertTrue( s.get_active(2) is f4 )
        self.assertTrue( s.get_active(99) is f4 )




if __name__ == '__main__':
    unittest.main()
