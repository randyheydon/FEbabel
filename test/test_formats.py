#!/usr/bin/env python2
from __future__ import with_statement

import unittest, xml.etree.ElementTree as etree
try: from cStringIO import StringIO
except: from StringIO import StringIO

import sys, os; sys.path[0] = os.path.dirname(sys.path[0])
import febabel as f


class TestFeb(unittest.TestCase):


    def test_writer(self):
        p = f.problem.FEproblem()
        Node = f.geometry.Node
        nodes = [
            Node((0,0,0)), Node((1,0,0)), Node((1,1,0)), Node((0,1,0)),
            Node((0,0,1)), Node((1,0,1)), Node((1,1,1)), Node((0,1,1)),
            Node((0,0,2)), Node((1,0,2)), Node((1,1,2)), Node((0,1,2)),
        ]
        p.elements.add(f.geometry.Hex8(nodes[0:8]))
        p.elements.add(f.geometry.Hex8(nodes[4:12]))

        outfile = StringIO()
        p.write_feb(outfile)

        # Check the resulting XML.
        tree = etree.fromstring(outfile.getvalue())

        nodes = tree.find('Geometry').find('Nodes').findall('node')
        self.assertEqual(len(nodes), 12)
        # All nodes are properly numbered.
        self.assertEqual([n.get('id') for n in nodes], map(str, range(1,13)))

        elements = tree.find('Geometry').find('Elements').findall('hex8')
        self.assertEqual(len(elements), 2)
        self.assertEqual([e.get('id') for e in elements], ['1','2'])
        # The two elements share four nodes (but element order can't be assured).
        e0 = elements[0].text.split(',')
        e1 = elements[1].text.split(',')
        self.assertTrue(e0[4:8] == e1[0:4] or e1[4:8] == e0[0:4])



class TestInp(unittest.TestCase):


    def test_reader(self):
        p = f.problem.FEproblem()
        with open(os.path.join(os.path.dirname(__file__), 'data', 'tf_joint.inp')) as inp:
            p.read_inp(inp)
        self.assertEqual(len(p.sets['tf_joint.inp']['nodes']), 96853)
        self.assertEqual(len(p.sets['tf_joint.inp']['elements']), 81653)




if __name__=='__main__':
    unittest.main()
