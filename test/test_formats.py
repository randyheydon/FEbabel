#!/usr/bin/env python2
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
        self.assertTrue(elements[0].text[8:15] == elements[1].text[0:7] or
            elements[1].text[8:15] == elements[0].text[0:7])




if __name__=='__main__':
    unittest.main()
