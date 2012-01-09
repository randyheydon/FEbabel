#!/usr/bin/env python2
import unittest
from math import sqrt

import sys, os
# For Python 3, use the translated version of the library.
# For Python 2, find the library one directory up.
if sys.version < '3':
    sys.path.append(os.path.dirname(sys.path[0]))
import febabel as f
m = f.materials


class TestMaterials(unittest.TestCase):


    def test_parameter_storing(self):
        l = m.LinearIsotropic(12.5, 15)
        self.assertEqual(l.E, 12.5)
        self.assertEqual(l.v, 15)
        mr = m.MooneyRivlin(1,4,9)
        self.assertEqual(mr.c1, 1)
        self.assertEqual(mr.c2, 4)
        self.assertEqual(mr.k, 9)



class TestAxes(unittest.TestCase):
    def setUp(self):
        h = f.geometry.Hex8
        n = f.geometry.Node
        self.elements = [
            h( [n((1,1,1)), n((2,1,1)), n((2,2,1)), n((1,2,1)),
                n((1,1,2)), n((2,1,2)), n((2,2,2)), n((1,2,2))] ),
            h( [n((0,4,3))] * 8 )
        ]

    def assertArrayAlmostEqual(self, a, b):
        '''Convenience function for testing arrays of inexact floats.'''
        self.assertArrayEqual(a, b, almost=True)

    def assertArrayEqual(self, a, b, n=[], almost=False):
        '''Convenience function for testing arrays exactly.'''
        if hasattr(a, '__getitem__') and hasattr(b, '__getitem__'):
            n = n[:]; n.append(0)
            for m,(i,j) in enumerate(zip(a,b)):
                n[-1] = m
                self.assertArrayEqual(i,j, n, almost)
        else:
            f = self.assertEqual if not almost else self.assertAlmostEqual
            f(a,b, msg='Elements differ at %s' % n)


    def test_normalization(self):
        self.assertArrayAlmostEqual( m.AxisOrientation._normalize([1,0,0],[0,1,0]),
            ([1,0,0],[0,1,0],[0,0,1]) )
        self.assertArrayAlmostEqual( m.AxisOrientation._normalize([1,0,0],[0.234,1,0]),
            ([1,0,0],[0,1,0],[0,0,1]) )
        self.assertArrayAlmostEqual( m.AxisOrientation._normalize([3,4,0],[3,4,1]),
            ([0.6, 0.8, 0], [0,0,1], [0.8, -0.6, 0]) )

        vs = m.AxisOrientation._normalize([2.312211, 745.3442, 3.505], [543, 1.1, 1.2])
        for v in vs:
            length = sqrt( sum( i*i for i in v) )
            self.assertAlmostEqual(length, 1,
                msg='Basis vector is not unit length!')
        for va in vs:
            for vb in vs:
                if not (va is vb):
                    dot = sum( i*j for i,j in zip(va, vb) )
                    self.assertAlmostEqual(dot, 0,
                        msg='Basis vectors are not orthogonal!')


    def test_vector_orientation(self):
        self.assertEqual(
            m.VectorOrientation([1,0,0],[0,1,0]).get_at_element(self.elements[0]),
            ([1,0,0],[0,1,0],[0,0,1]) )
        self.assertEqual(
            m.VectorOrientation([1,0,0],[0.234,1,0]).get_at_element(self.elements[0]),
            ([1,0,0],[0,1,0],[0,0,1]) )
        self.assertEqual(
            m.VectorOrientation([3,4,0],[3,4,1]).get_at_element(self.elements[0]),
            ([0.6, 0.8, 0], [0,0,1], [0.8, -0.6, 0]) )


    def test_spherical_orientation(self):
        self.assertEqual(
            m.SphericalOrientation([0,0,0],[0,0,1]).get_at_element(self.elements[1]),
            ([0, 0.8, 0.6], [0, -0.6, 0.8], [1,0,0]) )
        # Imprecision in the floats makes standard equality fail here.
        self.assertArrayAlmostEqual(
            m.SphericalOrientation([0,0,0],[0,0,1]).get_at_element(self.elements[0]),
            ([1/sqrt(3), 1/sqrt(3), 1/sqrt(3)], [-1/sqrt(6), -1/sqrt(6), sqrt(2.0/3)],
                [1/sqrt(2), -1/sqrt(2), 0]) )


    def test_nodal_orientation(self):
        self.assertEqual(
            m.NodalOrientation((0,1),(0,3)).get_at_element(self.elements[0]),
            ([1,0,0],[0,1,0],[0,0,1]) )
        self.assertEqual(
            m.NodalOrientation((0,1),(0,2)).get_at_element(self.elements[0]),
            ([1,0,0],[0,1,0],[0,0,1]) )
        self.assertEqual(
            m.NodalOrientation((0,1),(1,2)).get_at_element(self.elements[0]),
            ([1,0,0],[0,1,0],[0,0,1]) )
        self.assertEqual(
            m.NodalOrientation((0,1),(0,4)).get_at_element(self.elements[0]),
            ([1,0,0],[0,0,1],[0,-1,0]) )




if __name__ == '__main__':
    unittest.main()
