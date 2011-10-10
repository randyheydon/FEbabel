"""
Contains a method for writing an FEproblem to FEBio's .feb format.

Supports .feb version 1.1.
"""


def write(self, file_name_or_obj):
    """Write out the current problem state to an FEBio .feb file.
    NOTE: Not all nuances of the state can be fully represented."""

    import xml.etree.ElementTree as etree

    e_root = etree.Element('febio_spec',
        {'version': supported_writers['FEBio']})

    e_control = etree.SubElement(e_root, 'Control')
    # TODO: Control stuff.

    e_material = etree.SubElement(e_root, 'Material')
    # TODO: Material stuff.

    e_geometry = etree.SubElement(e_root, 'Geometry')
    nodes = set()
    for e in self.elements:
        nodes.update(iter(e))
    nodelist = list(nodes)

    e_nodes = etree.SubElement(e_geometry, 'Nodes')
    for i,n in enumerate(nodelist):
        e_node = etree.SubElement(e_nodes, 'node', {'id':str(i+1)})
        e_node.text = ','.join( map(str,iter(n)) )

    e_elements = etree.SubElement(e_geometry, 'Elements')
    for i,e in enumerate(self.elements):
        e_elem = etree.SubElement(e_elements, 'AN ELEMENT',
            {id:str(i+1), 'mat':'A MATERIAL'})
        # TODO: Mapping between internal and FEBio element types.
        # TODO: Materials listing.
        e_elem.text = ','.join( str(nodelist.index(n)+1)
            for n in iter(e) )

    etree.ElementTree(root).write(file_name_or_obj)
