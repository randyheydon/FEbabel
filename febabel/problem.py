from __future__ import with_statement
import os
from itertools import chain

from .common import Base, Constrainable
from . import geometry as geo, materials as mat, constraints as con


class FEproblem(Base):
    """A class to contain an entire finite element problem description."""

    def __init__(self):
        self.options = dict()
        self.sets = dict()

    def get_children(self):
        return set(chain( *self.sets.values() ))


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

    def get_constrainables(self):
        "Returns the set of all constrainable objects."
        # TODO: Search each set directly for constrainables?
        constrainable = set()
        for c in chain(self.get_nodes(), self.get_elements(), self.get_materials()):
            if isinstance(c, Constrainable):
                constrainable.add(c)
        return constrainable

    def get_constraints(self):
        """Returns all constraints applied to constrainable objects.
        Does not include None."""
        # TODO: Search each set directly for constraints?
        constraints = set()
        for constrainable in self.get_constrainables():
            constraints.update( c for c in constrainable.constraints.values()
                if isinstance(c, con.Constraint) )
        return constraints

    def get_loadcurves(self):
        "Returns all loadcurves applied to constraints."
        # TODO: Search each set directly for loadcurves?
        loadcurves = set()
        for cons in self.get_constraints():
            if isinstance(cons, con.Switch):
                loadcurves.update( x.loadcurve for x in
                    cons.points.itervalues() if isinstance(x, con.Constraint) )
            else:
                loadcurves.add(cons.loadcurve)
        return loadcurves


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
