"""
Contains a method for writing an FEproblem to FEBio's .feb format.

Supports .feb version 1.1.
"""

from .. import geometry as g

# Map internal element types to the FEBio identifier to which they're written.
# Spring and surface elements are handled differently, so not included.
element_write_map = {
    g.Tet4: 'tet4',
    g.Pent6: 'pent6',
    g.Hex8: 'hex8',
    g.Shell3: 'tri3',
    g.Shell4: 'quad4',
}

# Map for reading is generally the inverse of above, but can be modified
# separately by users if they have made custom element types.
#element_read_map = dict((v,k) for k,v in element_write_map.iteritems())
#del element_read_map[None]


def write(self, file_name_or_obj):
    """Write out the current problem state to an FEBio .feb file.
    NOTE: Not all nuances of the state can be fully represented."""

    import xml.etree.ElementTree as etree

    e_root = etree.Element('febio_spec',
        {'version': '1.1'})

    e_control = etree.SubElement(e_root, 'Control')
    # TODO: Control stuff.

    e_material = etree.SubElement(e_root, 'Material')
    # TODO: Material stuff.

    e_geometry = etree.SubElement(e_root, 'Geometry')
    nodes = list(self.get_nodes())

    e_nodes = etree.SubElement(e_geometry, 'Nodes')
    for i,n in enumerate(nodes):
        e_node = etree.SubElement(e_nodes, 'node', {'id':str(i+1)})
        e_node.text = ','.join( map(str,iter(n)) )

    e_elements = etree.SubElement(e_geometry, 'Elements')
    # Get list of only those elements that FEBio lists in the Elements section.
    elements = [e for e in self.elements if type(e) in element_write_map]
    for i,e in enumerate(elements):
        e_elem = etree.SubElement(e_elements, element_write_map[type(e)],
            {'id':str(i+1), 'mat':'A MATERIAL'})
        # TODO: Materials listing.
        e_elem.text = ','.join( str(nodes.index(n)+1)
            for n in iter(e) )

    etree.ElementTree(e_root).write(file_name_or_obj)
