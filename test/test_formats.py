#!/usr/bin/env python2
import unittest
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
        p.elements.extend(
            [f.geometry.Hex8(nodes[0:8]), f.geometry.Hex8(nodes[4:12])] )

        outfile = StringIO()
        p.write_feb(outfile)
        print outfile.getvalue()




if __name__=='__main__':
    unittest.main()
