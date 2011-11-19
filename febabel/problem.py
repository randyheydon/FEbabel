from __future__ import with_statement
import os
from itertools import chain

from . import geometry as geo, materials as mat


class FEproblem(object):
    """A class to contain an entire finite element problem description."""

    def __init__(self):
        self.options = dict()
        self.sets = dict()


    def get_nodes(self):
        "Returns the set of all nodes found in sets and elements."
        nodes = set( x for x in chain(*self.sets.values())
            if isinstance(x, geo.Node) )
        for e in self.get_elements():
            nodes.update(iter(e))
        return nodes

    def get_elements(self):
        "Returns the set of all elements found in the problem's sets."
        return set( x for x in chain(*self.sets.values())
            if isinstance(x, geo.Element) )

    def get_materials(self):
        "Returns the set of all materials found in sets and elements."
        materials = set( x for x in chain(*self.sets.values())
            if isinstance(x, mat.Material) )
        materials.update( e.material for e in self.get_elements() )
        materials.discard(None)
        return materials


    def read(self, filename):
        """Convenience function to run the appropriate reader method.
        Currently guesses based on file extension."""
        ext = os.path.splitext(filename)[1][1:]
        getattr(self, 'read_%s'%ext)(filename)

    def write(self, filename):
        """Convenience function to run the appropriate writer method.
        Currently guesses based on file extension."""
        ext = os.path.splitext(filename)[1][1:]
        getattr(self, 'write_%s'%ext)(filename)
