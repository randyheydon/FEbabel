#!/usr/bin/env python2
from __future__ import with_statement

import unittest, xml.etree.ElementTree as etree

import sys, os
# For Python 3, use the translated version of the library.
# For Python 2, find the library one directory up.
if sys.version > '3':
    from io import BytesIO as StringIO
else:
    try: from cStringIO import StringIO
    except: from StringIO import StringIO
    sys.path.append(os.path.dirname(sys.path[0]))

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
        self.assertEqual([n.get('id') for n in nodes],
            [str(i) for i in range(1,13)])

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
        # Check all nodes and elements are accounted for.
        self.assertEqual(len( [n for n in p.sets['tf_joint.inp'].keys()
            if n.startswith('node')] ), 96853)
        self.assertEqual(len( [e for e in p.sets['tf_joint.inp'].keys()
            if e.startswith('element')] ), 81653)
        # Check sets have found the correct nodes/elements.
        self.assertTrue( list(p.sets['tf_joint.inp']['node25225'])[0] in
            p.sets['tf_joint.inp']['f2fem'])
        self.assertFalse( list(p.sets['tf_joint.inp']['node1032'])[0] in
            p.sets['tf_joint.inp']['f2fem'])
        self.assertTrue( list(p.sets['tf_joint.inp']['element52864'])[0] in
            p.sets['tf_joint.inp']['acl'])
        self.assertFalse( list(p.sets['tf_joint.inp']['element9433'])[0] in
            p.sets['tf_joint.inp']['acl'])
        # Check all sets are accounted for.
        for xset in ('f2fem', 'tc2tib', 'tiblig', 'femlig', 'lmant', 'lmpost',
            'mmant', 'mmpost', 'femur', 'tibia', 'fcart', 'fcartr', 'fcartb',
            'fcartm', 'fcartt', 'tcart', 'tcartb', 'tcartm', 'tcartt', 'mcl',
            'amc', 'mmc', 'pmc', 'lcl', 'alc', 'mlc', 'plc', 'lat meni',
            'med meni', 'pcl', 'apc', 'ppc', 'acl', 'aclfiber', 'aac', 'pac'):
            self.assertTrue( xset in p.sets['tf_joint.inp'].keys(),
                msg='Set %s not found' % xset )




if __name__=='__main__':
    unittest.main()