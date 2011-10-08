from .constraints import Constrainable


class Material(object):
    "Base material object."

class ElasticIsotropic(Material): pass
class Linear(ElasticIsotropic): pass
class MooneyRivlin(ElasticIsotropic): pass
class Ogden(ElasticIsotropic): pass

class Porous(Material):
    def __init__(self, porosity, base):
        pass

class Rigid(Material, Constrainable):
    def __init__(self, COM=None):
        Material.__init__(self)
        Constrainable.__init__(self)
