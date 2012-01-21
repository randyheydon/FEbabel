#!/usr/bin/env python2
import unittest

import sys, os
# For Python 3, use the translated version of the library.
# For Python 2, find the library one directory up.
if sys.version < '3':
    sys.path.append(os.path.dirname(sys.path[0]))
import febabel as f    

datadir = os.path.join(os.path.dirname(__file__), 'data')


class TestCnfg(unittest.TestCase):


    def test_read_cnfg(self):
        p = f.problem.FEproblem()
        p.read_cnfg(os.path.join(datadir, 'meniscectomy_kurosawa80.cnfg'))

        # Check tf_joint.inp's elements and nodes are present.
        # NOTE: Nodes are moved from their original tf_joint.inp positions.
        # This is checked visually. TODO: Proper transformation test.
        self.assertEqual(len(p.sets['tf_joint.inp:allnodes']), 96853)
        self.assertEqual(len(p.sets['tf_joint.inp:allelements']), 81653)

        descendants = p.get_descendants_sorted()
        # This check gets thrown way off by the unique material in each spring.
        #self.assertEqual(len(descendants[f.materials.Material]), 15+5)

        # Find each material in the elements of its corresponding set.
        # Ensure all elements in the set have the same material, then test it.
        for eset in ('femur', 'tibia'):
            s = set(e.material for e in p.sets['tf_joint.inp:%s'%eset])
            self.assertEqual(len(s), 1)
            m = s.pop()
            self.assertEqual(type(m), f.materials.Rigid)
            self.assertEqual(m.density, 1.132e-6)
            self.assertEqual(m.center_of_mass, [0,0,0])
        for eset in ('fcartb', 'fcartm', 'fcartt', 'tcartb', 'tcartm', 'tcartt'):
            s = set(e.material for e in p.sets['tf_joint.inp:%s'%eset])
            self.assertEqual(len(s), 1)
            m = s.pop()
            self.assertEqual(type(m), f.materials.MooneyRivlin)
            #self.assertEqual(m.density, 1.5e-9)
            self.assertEqual(m.c1, 0.856)
            self.assertEqual(m.c2, 0)
            self.assertEqual(m.k, 8)
        for eset in ('lat meni', 'med meni'):
            s = set(e.material for e in p.sets['tf_joint.inp:%s'%eset])
            self.assertEqual(len(s), 1)
            m = s.pop()
            self.assertEqual(type(m), f.materials.FungOrthotropic)
            #self.assertEqual(m.density, 1.5e-9)
            self.assertEqual(m.E1, 125)
            self.assertEqual(m.E2, 27.5)
            self.assertEqual(m.E3, 27.5)
            self.assertEqual(m.v12, 0.1)
            self.assertEqual(m.v23, 0.33)
            self.assertEqual(m.v31, 0.1)
            self.assertEqual(m.G12, 2)
            self.assertEqual(m.G23, 12.5)
            self.assertEqual(m.G31, 2)
            self.assertEqual(m.c, 1)
            self.assertEqual(m.k, 10)
            self.assertEqual(m.axis.edge1, [6,7])
            self.assertEqual(m.axis.edge2, [6,2])
        for eset in ('acl', 'aclfiber'):
            s = set(e.material for e in p.sets['tf_joint.inp:%s'%eset])
            #self.assertEqual(len(s), 1) # FIXME: Why does this fail on acl?
            m = s.pop()
            self.assertEqual(type(m), f.materials.TransIsoElastic)
            #self.assertEqual(m.density, 1.5e-9)
            self.assertEqual(m.c3, 0.0139)
            self.assertEqual(m.c4, 116.22)
            self.assertEqual(m.c5, 535.039)
            self.assertEqual(m.lam_max, 1.046)
            self.assertEqual(m.axis.edge1, [0,3])
            self.assertEqual(type(m.base), f.materials.MooneyRivlin)
            self.assertEqual(m.base.c1, 1.95)
            self.assertEqual(m.base.c2, 0)
            self.assertEqual(m.base.k, 73.2)
        s = set(e.material for e in p.sets['tf_joint.inp:pcl'])
        self.assertEqual(len(s), 1)
        m = s.pop()
        self.assertEqual(type(m), f.materials.TransIsoElastic)
        #self.assertEqual(m.density, 1.5e-9)
        self.assertEqual(m.c3, 0.1196)
        self.assertEqual(m.c4, 87.178)
        self.assertEqual(m.c5, 431.063)
        self.assertEqual(m.lam_max, 1.035)
        self.assertEqual(m.axis.edge1, [0,3])
        self.assertEqual(type(m.base), f.materials.MooneyRivlin)
        self.assertEqual(m.base.c1, 3.25)
        self.assertEqual(m.base.c2, 0)
        self.assertEqual(m.base.k, 122)
        for eset in ('mcl', 'lcl'):
            s = set(e.material for e in p.sets['tf_joint.inp:%s'%eset])
            self.assertEqual(len(s), 1)
            m = s.pop()
            self.assertEqual(type(m), f.materials.TransIsoElastic)
            #self.assertEqual(m.density, 1.5e-9)
            self.assertEqual(m.c3, 0.57)
            self.assertEqual(m.c4, 48)
            self.assertEqual(m.c5, 467.1)
            self.assertEqual(m.lam_max, 1.063)
            self.assertEqual(m.axis.edge1, [0,3])
            self.assertEqual(type(m.base), f.materials.MooneyRivlin)
            self.assertEqual(m.base.c1, 1.44)
            self.assertEqual(m.base.c2, 0)
            self.assertEqual(m.base.k, 397)

        # Check that constraints are applied properly to the rigid bodies.
        from febabel.constraints import free, fixed
        mtibia = list( p.sets['tf_joint.inp:tibia'] )[0].material
        self.assertTrue( isinstance(mtibia.constraints['Rx'],
            f.constraints.SwitchConstraint) )
        for dof in ('x','y','z','Rx','Ry','Rz'):
            self.assertEqual(mtibia.constraints[dof].points, {0:fixed})

        mfemur = list( p.sets['tf_joint.inp:femur'] )[0].material
        self.assertTrue( isinstance(mfemur.constraints['Rx'],
            f.constraints.SwitchConstraint) )
        self.assertEqual(mfemur.constraints['x'].points, {0:free})
        self.assertEqual(mfemur.constraints['y'].points, {0:free})
        self.assertEqual(mfemur.constraints['Rx'].points, {0:fixed})
        self.assertEqual(mfemur.constraints['Ry'].points, {0:free})
        self.assertEqual(mfemur.constraints['Rz'].points, {0:fixed})

        force = mfemur.constraints['z'].points[0]
        self.assertTrue( isinstance(force, f.constraints.Force) )
        self.assertEqual(force.multiplier, 1.0)
        lc = force.loadcurve
        self.assertEqual(lc.interpolation, f.constraints.LoadCurve.IN_LINEAR)
        self.assertEqual(lc.points, {0:0, 0.1:-10, 0.4:-500, 0.7:-1000, 1:-1500})

        # Check that rigid interfaces have been created.
        rigid_ints = list(p.sets['meniscectomy_kurosawa80.cnfg:rigid_int'])
        self.assertEqual(len(rigid_ints), 4)
        for i in rigid_ints:
            self.assertTrue(isinstance(i, f.constraints.RigidInterface))
        self.assertTrue(len([i for i in rigid_ints if i.rigid_body is mtibia]), 2)
        self.assertTrue(len([i for i in rigid_ints if i.rigid_body is mfemur]), 2)
        self.assertTrue(len([i for i in rigid_ints if
                             i.nodes == p.sets['tf_joint.inp:f2fem']]), 1)
        self.assertTrue(len([i for i in rigid_ints if
                             i.nodes == p.sets['tf_joint.inp:tc2tib']]), 1)
        self.assertTrue(len([i for i in rigid_ints if
                             i.nodes == p.sets['tf_joint.inp:tiblig']]), 1)
        self.assertTrue(len([i for i in rigid_ints if
                             i.nodes == p.sets['tf_joint.inp:femlig']]), 1)

        # Check contact interfaces have been created.
        contact = list(p.sets['meniscectomy_kurosawa80.cnfg:contact'])
        self.assertEqual(len(contact), 3)
        self.assertTrue(len([i for i in contact if
                             i.master == p.sets['tf_joint.inp:fcsm']]), 1)
        self.assertTrue(len([i for i in contact if
                             i.master == p.sets['tf_joint.inp:fcsl']]), 1)
        self.assertTrue(len([i for i in contact if
                             i.master == p.sets['tf_joint.inp:aclsurf']]), 1)
        self.assertTrue(len([i for i in contact if
                             i.slave == p.sets['tf_joint.inp:tcsm']]), 1)
        self.assertTrue(len([i for i in contact if
                             i.slave == p.sets['tf_joint.inp:tcsl']]), 1)
        self.assertTrue(len([i for i in contact if
                             i.slave == p.sets['tf_joint.inp:pclsurf']]), 1)

        # Check spring elements have been created.
        self.assertEqual(len(
            p.sets['meniscectomy_kurosawa80.cnfg:latant_horn'] ), 88)
        self.assertEqual(len(
            p.sets['meniscectomy_kurosawa80.cnfg:latpost_horn'] ), 88)
        self.assertEqual(len(
            p.sets['meniscectomy_kurosawa80.cnfg:medant_horn'] ), 88)
        self.assertEqual(len(
            p.sets['meniscectomy_kurosawa80.cnfg:medpost_horn'] ), 88)




if __name__=='__main__':
    unittest.main()
