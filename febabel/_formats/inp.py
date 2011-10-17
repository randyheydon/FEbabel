"""
Contains a method for reading Abaqus's .inp format and to add to an FEproblem.
"""
import os
from warnings import warn

from .. import geometry as g
from ._common import ValsDict, SETSEP, NSET, ESET


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
            nodelist = ValsDict()
            self.sets[SETSEP.join((name,NSET))] = nodelist

            l = fileobj.readline()
            while not (l.startswith('*') or l==''):
                v = l.split(',')
                nodelist[v[0]] = g.Node( map(float, v[1:4]) )
                l = fileobj.readline()

        elif l.startswith('*ELEMENT,TYPE='):
            # Parse element.  Determine its type and node numbers.
            # TODO: Can shell element thickness be read from .inp files?
            eset_name = SETSEP.join((name,ESET))
            if eset_name in self.sets:
                elemlist = self.sets[eset_name]
            else:
                elemlist = ValsDict()
                self.sets[eset_name] = elemlist
            nodelist = self.sets[SETSEP.join((name,NSET))]

            etype = element_read_map[ l.strip().split('=')[1] ]
            l = fileobj.readline()
            while not (l.startswith('*') or l==''):
                v = l.strip().split(',')
                elemlist[v[0]] = etype( nodelist[i] for i in v[1:] )
                l = fileobj.readline()

        elif l.startswith('*NSET,NSET=') or l.startswith('*ELSET,ELSET='):
            # FIXME: Check that xset_name is not 'nodes' or 'elements', used
            # above.  Or use some different method above.
            xset_name = l.strip().split('=',1)[1]
            group = SETSEP.join((name, NSET if l.startswith('*NSET') else ESET))

            l = fileobj.readline()
            lines = list()
            while not (l.startswith('*') or l==''):
                lines.append(l.strip())
                l = fileobj.readline()

            self.sets[SETSEP.join((name,xset_name))] = set( self.sets[group][i]
                for i in ''.join(lines).split(',') )

        else:
            warn('Unrecognized section "%s".  Skipping remainder of file.'
                % l.strip())
            break
