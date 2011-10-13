from .constraints import Constrainable



class Material(object):
    "Base material object."

    def _store(self, params):
        del params['self']
        for k,v in params.iteritems():
            setattr(self, k, v)



class LinearIsotropic(Material):
    def __init__(self, E, v):
        self._store(locals())

class NeoHookean(Material):
    def __init__(self, E, v):
        self._store(locals())

class MooneyRivlin(Material):
    def __init__(self, c1, c2, k):
        self._store(locals())

class Ogden(Material):
    def __init__(ci, mi, k, laugon=False, atol=0.01):
        self._store(locals())

class Porous(Material):
    def __init__(self, porosity, base):
        self._store(locals())

class Rigid(Material, Constrainable):
    def __init__(self, COM=None):
        Constrainable.__init__(self)
        self._store(locals())
