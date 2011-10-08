class Constrainable(object):
    "A mixin to allow different object types to accept constraints."
    def __init__(self, **kwargs):
        self.constraints = list()
        super(Constrainable, self).__init__(**kwargs)

class Switchable(object):
    "A mixin to allow an object to be turned on or off at specific times."



class LoadCurve(object):
    ""

# TODO: a few common loadcurves
loadcurve_zero = LoadCurve()
loadcurve_instant = LoadCurve()



class Constraint(Switchable):
    "Base class for different types of constraints/loads."

    def __init__(self, vector, loadcurve, **kwargs):
        super(Constraint, self).__init__(**kwargs)


class Force(Constraint): pass
class Displacement(Constraint): pass
class Fixed(Displacement):
    def __init__(self):
        super(Fixed, self).__init__(self, (0,0,0), loadcurve_zero)



