class Constrainable(object):
    "A mixin to allow different object types to accept constraints."
    def __init__(self):
        self.constraints = list()

class Switchable(object):
    "A mixin to allow an object to be activated at specific times."



class LoadCurve(object):
    ""

# TODO: a few common loadcurves
loadcurve_zero = LoadCurve()
loadcurve_instant = LoadCurve()



class Constraint(Switchable):
    "Base class for different types of constraints/loads."

    def __init__(self, vector, loadcurve, **kwargs):
        Switchable.__init__(self)


class Force(Constraint): pass
class Displacement(Constraint): pass
class Fixed(Displacement):
    def __init__(self):
        Displacement.__init__(self, (0,0,0), loadcurve_zero)



