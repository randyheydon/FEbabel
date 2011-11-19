"""
Contains a method for reading Abaqus's .inp format and to add to an FEproblem.
"""
from __future__ import with_statement
import os
from warnings import warn

from .. import geometry as g, problem
from ._common import ValsDict, SETSEP, NSET, ESET


element_read_map = {
    'C3D8': g.Hex8,
    'S4': g.Shell4,
    # TODO: Add support for tetrahedra, triangular shells, others needed?
}


def read(self, filename):
    """Read a file in Abaqus's .inp format into the current problem.
    NOTE: This cannot yet handle anything beyond brick and shell elements, and
    who knows what other crazy features of the format."""

    # TODO: Test if name is already used; modify it if so?
    name = os.path.basename(filename)

    # Store all sets defined in this file under a sub-dict.
    self.sets[name] = dict()

    with open(filename) as fileobj:
        l = fileobj.readline()
        while l != '':

            if l.startswith('*NODE'):
                # Parse node coordinates and add to file's default nodeset.
                # Store nodes in a ValsDict so they can individually be accessed by
                # the IDs given to them in the file.
                nodelist = ValsDict()
                self.sets[SETSEP.join((name,NSET))] = nodelist

                l = fileobj.readline()
                while not (l.startswith('*') or l==''):
                    v = l.split(',')
                    nodelist[v[0]] = g.Node( map(float, v[1:4]) )
                    l = fileobj.readline()

            elif l.startswith('*ELEMENT,TYPE='):
                # Parse element.  Determine its type and nodes.
                # Elements are defined in multiple sections, so don't overwrite the
                # ValsDict if it already exists.
                eset_name = SETSEP.join((name,ESET))
                if eset_name in self.sets:
                    elemlist = self.sets[eset_name]
                else:
                    elemlist = ValsDict()
                    self.sets[eset_name] = elemlist
                nodelist = self.sets[SETSEP.join((name,NSET))]

                # TODO: Can shell element thickness be read from .inp files?
                etype = element_read_map[ l.strip().split('=')[1] ]
                l = fileobj.readline()
                while not (l.startswith('*') or l==''):
                    v = l.strip().split(',')
                    elemlist[v[0]] = etype( nodelist[i] for i in v[1:] )
                    l = fileobj.readline()

            elif l.startswith('*NSET,NSET=') or l.startswith('*ELSET,ELSET='):
                # Parse the named node and element sets.
                # FIXME: Check that xset_name is not NSET or ESET.
                xset_name = SETSEP.join((name, l.strip().split('=',1)[1]))
                group = SETSEP.join((name, NSET if l.startswith('*NSET') else ESET))

                l = fileobj.readline()
                lines = list()
                while not (l.startswith('*') or l==''):
                    lines.append(l.strip())
                    l = fileobj.readline()

                self.sets[xset_name] = set( self.sets[group][i] for i in
                    ''.join(lines).split(',') )

            elif l.startswith('*SURFACE,NAME='):
                # Parse surface set.
                # Each surface element is defined by the element to which it's
                # attached, and the specific face it covers.
                # TODO: Support tetrahedra, triangular shells.
                surflist = set()
                self.sets[SETSEP.join((name, l.strip().split('=',1)[1]))] = surflist
                elemlist = self.sets[SETSEP.join((name, ESET))]

                # Pick off the nodes covered by each surface element, then
                # construct the surface element and add to the set.
                l = fileobj.readline()
                while not (l.startswith('*') or l==''):
                    element, side = l.strip().split(',')
                    e = elemlist[element]
                    if side == 'S1' or side == 'SPOS' or side == 'SNEG':
                        face = [ e[0], e[3], e[2], e[1] ]
                    elif side == 'S2':
                        face = [ e[4], e[5], e[6], e[7] ]
                    elif side == 'S3':
                        face = [ e[0], e[1], e[5], e[4] ]
                    elif side == 'S4':
                        face = [ e[1], e[2], e[6], e[5] ]
                    elif side == 'S5':
                        face = [ e[2], e[3], e[7], e[6] ]
                    elif side == 'S6':
                        face = [ e[0], e[4], e[7], e[3] ]
                    else:
                        warn('Bad face identifier: %s' % side)
                        continue
                    # TODO: Have it detect and reuse Surface elements?
                    surflist.add( g.Surface4(face) )
                    l = fileobj.readline()


            else:
                warn('Unrecognized section "%s".  Skipping remainder of file.'
                    % l.strip())
                break

problem.FEproblem.read_inp = read
