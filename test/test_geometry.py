#!/usr/bin/env python2
import unittest

import sys, os
# For Python 3, use the translated version of the library.
# For Python 2, find the library one directory up.
if sys.version < '3':
    sys.path.append(os.path.dirname(sys.path[0]))
from febabel import geometry as g


class TestNode(unittest.TestCase):


    def test_init(self):
        a = g.Node((3,4.5,9))


    def test_getters(self):
        pos = (-1.1, 900.5, 12)
        a = g.Node(pos)
        self.assertEqual(a.x, pos[0])
        self.assertEqual(a.y, pos[1])
        self.assertEqual(a.z, pos[2])
        self.assertEqual(a[0], pos[0])
        self.assertEqual(a[1], pos[1])
        self.assertEqual(a[2], pos[2])
        self.assertEqual(list(a), list(pos))


    def test_setters(self):
        pos = (0,0.5,0.05)
        a = g.Node(pos)
        a.x = 3
        self.assertEqual(a.x, 3)
        a[0] = 12
        self.assertEqual(a.x, 12)
        a.y = 32.1
        a.z = 909
        self.assertEqual(list(a), [12,32.1,909])



class TestElements(unittest.TestCase):

    def setUp(self):
        self.nodes = [g.Node(map(float,(i,j,k)))
            for i in range(3) for j in range(3) for k in range(3)]


    def test_init(self):
        g.Surface3(self.nodes[0:3])
        g.Tet4(self.nodes[0:4])


    def test_getters(self):
        a = g.Tet4(self.nodes[0:4])
        for n in range(4):
            self.assertEqual(a[n], self.nodes[n])
        for i,j in zip(a, self.nodes):
            self.assertEqual(i, j)


    def test_math(self):
        self.assertEqual( g.Shell3( [g.Node((0,0,0)), g.Node((0,0,1.5)),
            g.Node((1,1,1))] ).get_vertex_avg(),
            (1.0/3, 1.0/3, 2.5/3) )
        # Not sure if using tuples instead of Node objects should be a feature,
        # but may as well test for it until I decide to get rid of it. 
        # NOTE: If you're looking here for documentation, I recommend against this!
        self.assertEqual( g.Shell3( [(0,0,0), (0,0,1.5),
            (1,1,1)] ).get_vertex_avg(),
            (1.0/3, 1.0/3, 2.5/3) )

        self.assertEqual( g.Tet4( [g.Node((0,0,0)), g.Node((0,0,1.5)),
            g.Node((1,1,1)), g.Node((1,2,0))] ).get_vertex_avg(),
            (0.5, 0.75, 2.5/4) )




if __name__ == '__main__':
    unittest.main()
