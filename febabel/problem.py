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
