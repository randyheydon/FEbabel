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
            # Parse node coordinates.  Each is wrapped in a list and added to
            # the file's set dictionary, using 'node%s' as its key (where %s is
            # its node ID number).
            storage = self.sets[name]

            l = fileobj.readline()
            while not (l.startswith('*') or l==''):
                v = l.split(',')
                storage['node%s' % v[0]] = set([g.Node( map(float, v[1:4]) )])
                l = fileobj.readline()

        elif l.startswith('*ELEMENT,TYPE='):
            # Parse element.  Determine its type and node numbers.
            # TODO: Can shell element thickness be read from .inp files?
            storage = self.sets[name]

            etype = element_read_map[ l.strip().split('=')[1] ]
            l = fileobj.readline()
            while not (l.startswith('*') or l==''):
                v = l.strip().split(',')
                storage['element%s' % v[0]] = set(
                    etype( iter(storage['node%s' % i]).next() for i in v[1:] ) )
                l = fileobj.readline()

        elif l.startswith('*NSET,NSET=') or l.startswith('*ELSET,ELSET='):
            # FIXME: Check that xset_name is not 'nodes' or 'elements', used
            # above.  Or use some different method above.
            xset_name = l.strip().split('=',1)[1]
            group = 'node%s' if l.startswith('*NSET') else 'element%s'

            l = fileobj.readline()
            lines = list()
            while not (l.startswith('*') or l==''):
                lines.append(l.strip())
                l = fileobj.readline()

            self.sets[name][xset_name] = set([ iter(self.sets[name][group%i]).next()
                for i in ''.join(lines).split(',') ])

        #elif l.startswith('*SURFACE,NAME='):
        #    xset_name = l.strip().split('=',1)[1]

        else:
            warn('Unrecognized section "%s".  Skipping remainder of file.'
                % l.strip())
            break
