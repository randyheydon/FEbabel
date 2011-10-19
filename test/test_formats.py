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
datadir = os.path.join(os.path.dirname(__file__), 'data')

import febabel as f


class TestFeb(unittest.TestCase):


    def test_write_feb(self):
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


    def test_read_inp(self):
        p = f.problem.FEproblem()
        p.read_inp(os.path.join(datadir, 'tf_joint.inp'))
        # Check all nodes and elements are accounted for.
        self.assertEqual(len(p.sets['tf_joint.inp:allnodes']), 96853)
        self.assertEqual(len(p.sets['tf_joint.inp:allelements']), 81653)
        self.assertEqual(len(p.elements), 81653 + 35604)
        # Check sets have found the correct nodes/elements.
        self.assertTrue( p.sets['tf_joint.inp:allnodes']['25225'] in
            p.sets['tf_joint.inp:f2fem'])
        self.assertFalse( p.sets['tf_joint.inp:allnodes']['1032'] in
            p.sets['tf_joint.inp:f2fem'])
        self.assertTrue( p.sets['tf_joint.inp:allelements']['52864'] in
            p.sets['tf_joint.inp:acl'])
        self.assertFalse( p.sets['tf_joint.inp:allelements']['9433'] in
            p.sets['tf_joint.inp:acl'])
        # Check all sets are accounted for.
        for xset in ('f2fem', 'tc2tib', 'tiblig', 'femlig', 'lmant', 'lmpost',
            'mmant', 'mmpost', 'femur', 'tibia', 'fcart', 'fcartr', 'fcartb',
            'fcartm', 'fcartt', 'tcart', 'tcartb', 'tcartm', 'tcartt', 'mcl',
            'amc', 'mmc', 'pmc', 'lcl', 'alc', 'mlc', 'plc', 'lat meni',
            'med meni', 'pcl', 'apc', 'ppc', 'acl', 'aclfiber', 'aac', 'pac',
            'femmcl', 'femlcl', 'mcltib', 'lcltib', 'fcs', 'fcsr', 'fcsm',
            'fcsl', 'tcs', 'tcsl', 'tcsm', 'mcls', 'mclsurf', 'lcls',
            'lclsurf', 'lmtib', 'lmfem', 'lmfemr', 'lmtibr', 'mmtib', 'mmfem',
            'mmfemr', 'mmtibr', 'pclsurf', 'aclsurf', ):
            self.assertTrue( 'tf_joint.inp:%s'%xset in p.sets,
                msg='Set %s not found' % xset )




if __name__=='__main__':
    unittest.main()
