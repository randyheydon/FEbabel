"""
Contains a method for reading Abaqus's .inp format and to add to an FEproblem.
"""
import os
from warnings import warn

from .. import geometry as g


element_read_map = {
    'C3D8': g.Hex8,
    'S4': g.Shell4,
    # TODO: inp supports more than these...
}


def read(self, fileobj, name=None):

    if name is None:
        # TODO: Test if name is already used; modify it if so?
        try:
            name = os.path.basename(fileobj.name)
        except AttributeError:
            name = '<???>'

    # Store all sets defined in this file under a sub-dict.
    self.sets[name] = dict()

    l = fileobj.readline()
    while l != '':

        if l.startswith('*NODE'):
            # Parse node coordinates and append to nodelist.
            nodelist = dict()
            self.sets[name]['nodes'] = nodelist

            l = fileobj.readline()
            while not (l.startswith('*') or l==''):
                v = l.split(',')
                nodelist[v[0]] = g.Node( map(float, v[1:4]) )
                l = fileobj.readline()

        elif l.startswith('*ELEMENT,TYPE='):
            # Parse element.  Determine its type and node numbers.
            # TODO: Can shell element thickness be read from .inp files?
            if not 'elements' in self.sets[name]:
                elemlist = dict()
                self.sets[name]['elements'] = elemlist
            else:
                elemlist = self.sets[name]['elements']
            nodelist = self.sets[name]['nodes']

            etype = element_read_map[ l.strip().split('=')[1] ]
            l = fileobj.readline()
            while not (l.startswith('*') or l==''):
                v = l.strip().split(',')
                elemlist[v[0]] = etype( nodelist[i] for i in v[1:] )
                l = fileobj.readline()

        else:
            warn('Unrecognized section "%s".  Skipping remainder of file.' % l.strip())
            break
