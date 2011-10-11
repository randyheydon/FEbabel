#!/usr/bin/env python
import unittest, os

import sys; sys.path[0] = os.path.dirname(sys.path[0])
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
            for i in xrange(3) for j in xrange(3) for k in xrange(3)]


    def test_init(self):
        g.Surface3(self.nodes[0:3])
        g.Tet4(self.nodes[0:4])


    def test_getters(self):
        a = g.Tet4(self.nodes[0:4])
        for n in xrange(4):
            self.assertEqual(a[n], self.nodes[n])
        for i,j in zip(a, self.nodes):
            self.assertEqual(i, j)




if __name__ == '__main__':
    unittest.main()
