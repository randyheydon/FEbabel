class LoadCurve(object):
    ""

# TODO: a few common loadcurves
loadcurve_zero = LoadCurve()
loadcurve_instant = LoadCurve()



class Constraint(object):
    "Base class for different types of constraints/loads."

    def __init__(self, vector, loadcurve):
        pass


class Force(Constraint): pass
class Displacement(Constraint): pass
class Fixed(Displacement):
    def __init__(self):
        Displacement.__init__(self, (0,0,0), loadcurve_zero)



class Constrainable(object):
    "A mixin to allow different object types to accept constraints."
