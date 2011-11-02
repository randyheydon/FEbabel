from __future__ import with_statement
import os


class FEproblem(object):
    """A class to contain an entire finite element problem description."""

    def __init__(self):
        self.elements = set()
        self.options = dict()
        self.sets = dict()


    def get_nodes(self):
        "Returns the set of all nodes found in elements."
        nodes = set()
        for e in self.elements:
            nodes.update(iter(e))
        return nodes


    def get_materials(self):
        "Returns the set of all materials found in elements."
        return set(e.material for e in self.elements)


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
