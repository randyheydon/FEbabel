import unittest

import sys, os
# For Python 3, use the translated version of the library.
# For Python 2, find the library one directory up.
if sys.version < '3':
    sys.path.append(os.path.dirname(sys.path[0]))
import febabel as f


class TestFEproblem(unittest.TestCase):


    def test_descendants(self):
        # Create a problem.
        p = f.problem.FEproblem()
        matl1 = f.materials.Ogden([1,2,3,4,5,6,7],[8,9,10,11,12,13,14], 2.2)
        matl2 = f.materials.TransIsoElastic(15,16,17,18,
            axis=f.materials.SphericalOrientation((0,0,0),(0,0,1)),
            base=f.materials.VerondaWestmann(19,20,21),
        )
        Node = f.geometry.Node
        nodes = [
            Node((0,0,0)), Node((1,0,0)), Node((1,1,0)), Node((0,1,0)),
            Node((0,0,1)), Node((1,0,1)), Node((1,1,1)), Node((0,1,1)),
            Node((0,0,2)), Node((1,0,2)), Node((1,1,2)), Node((0,1,2)),
        ]
        p.sets[''] = set((
            f.geometry.Hex8(nodes[0:8], matl1),
            f.geometry.Hex8(nodes[4:12], matl2) ))
        # TODO: Add in some constraints.

        # Test descendants are found correctly: two elements, one timestepper.
        children = p.get_children()
        self.assertEqual(len(children), 3)
        self.assertEqual(len([i for i in children if
                         isinstance(i, f.geometry.Element)]), 2)
        self.assertEqual(len([i for i in children if
                         isinstance(i, f.problem.TimeStepper)]), 1)

        desc = p.get_descendants()
        # 2 Elements, 12 Nodes, 3 Materials (1 base), 1 AxisOrientation,
        # 1 Constraint (free), 1 LoadCurve (loadcurve_zero), 1 TimeStepper.
        self.assertEqual(len(desc), 2 + 12 + 3 + 1 + 1 + 1 + 1)

        desc_s = p.get_descendants_sorted()
        self.assertEqual(len(desc_s[f.geometry.Element]), 2)
        self.assertEqual(len(desc_s[f.geometry.Node]), 12)
        self.assertEqual(len(desc_s[f.materials.Material]), 3)
        self.assertEqual(len(desc_s[f.constraints.LoadCurve]), 1)
        self.assertEqual(len(desc_s[f.constraints.Contact]), 0)
        self.assertEqual(len(desc_s[f.common.Constrainable]), 12)
        self.assertEqual(len(desc_s[f.common.Switch]), 0)
        self.assertEqual(len(desc_s[None]), 3)




if __name__ == '__main__':
    unittest.main()
