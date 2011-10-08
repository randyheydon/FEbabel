from __future__ import with_statement


# Dictionaries listing supported filetypes and versions.
supported_readers = {}

supported_writers = {
    'FEBio': '1.1'
}



class FEproblem(object):
    """A class to contain an entire finite element problem description."""

    def __init__(self):
        self.elements = list()
        self.options = dict()


    def read_inp(self, filename):
        "Import an Abaqus .inp file into the current problem."

        with open(filename) as f:
            pass
            # TODO: Read file.


    def write_feb(self, file_name_or_obj):
        """Write out the current problem state to an FEBio .feb file.
        NOTE: Not all nuances of the state can be fully represented."""

        import xml.etree.ElementTree as etree

        root = etree.Element('febio_spec',
            {'version': supported_writers['FEBio']})

        control = etree.SubElement(root, 'Control')
        # TODO: The rest.

        etree.ElementTree(root).write(file_name_or_obj)
