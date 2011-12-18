#!/usr/bin/env python2
import unittest

import sys, os
# For Python 3, use the translated version of the library.
# For Python 2, find the library one directory up.
if sys.version < '3':
    sys.path.append(os.path.dirname(sys.path[0]))
import febabel as f    

datadir = os.path.join(os.path.dirname(__file__), 'data')


class TestInp(unittest.TestCase):


    def test_read_inp(self):
        p = f.problem.FEproblem()
        p.read_inp(os.path.join(datadir, 'tf_joint.inp'))
        # Check all nodes and elements are accounted for.
        self.assertEqual(len(p.sets['tf_joint.inp:allnodes']), 96853)
        self.assertEqual(len(p.sets['tf_joint.inp:allelements']), 81653)
        self.assertEqual(len(p.get_elements()), 81653 + 35604)
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
