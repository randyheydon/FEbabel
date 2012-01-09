from __future__ import with_statement
import os
from itertools import chain

from .common import Base, Constrainable, Switch
from . import geometry as geo, materials as mat, constraints as con


class FEproblem(Base):
    """A class to contain an entire finite element problem description."""

    def __init__(self):
        self.options = dict()
        self.sets = dict()

    def get_children(self):
        return set(chain( *self.sets.values() ))


    # FIXME: Maybe this should be a method of Base?
    def get_descendants_sorted(self):
        """Returns all descendants, sorted into a dictionary by type.
        Descendants can by placed under multiple types (eg. Nodes will also end
        up in Constrainables).
        If a descendant is not any of the sorted types, it will be placed under
        None."""

        ds = {
            geo.Node: set(),
            geo.Element: set(),
            mat.Material: set(),
            Constrainable: set(),
            con.Constraint: set(),
            con.LoadCurve: set(),
            Switch: set(),
            None: set()
        }

        for x in self.get_descendants():
            placed = False
            for cls,st in ds.iteritems():
                if cls is not None and isinstance(x, cls):
                   st.add(x)
                   placed = True
            if not placed:
                ds[None].add(x)

        return ds


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
